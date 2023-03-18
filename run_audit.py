#!/usr/bin/env python3

import os
import subprocess
import time
import json

# Define Goss host variables
AUDIT_BIN = os.environ.get("AUDIT_BIN", "/usr/local/bin/goss")
AUDIT_FILE = os.environ.get("AUDIT_FILE", "goss.yml")
AUDIT_CONTENT_LOCATION = os.environ.get("AUDIT_CONTENT_LOCATION", "/home/ubuntu")

# Define Goss benchmark variables
BENCHMARK = "CIS"
BENCHMARK_VER = "1.1.0"
BENCHMARK_OS = "UBUNTU2004"

# Set default host system type
host_system_type = "Server"

# Pre-Checks: Ensure root privileges
if os.getuid() != 0:
    print("Script needs to run with root privileges")
    exit(1)

# Main Script

# Discover OS version
with open("/etc/os-release", "r") as os_release_file:
    os_release_data = os_release_file.read()

if "rhel" in os_release_data:
    os_vendor = "RHEL"
else:
    os_vendor = subprocess.check_output(
        "hostnamectl | grep Oper | cut -d : -f2 | awk '{print $1}' | tr a-z A-Z",
        shell=True,
        text=True,
    ).strip()

os_maj_ver = (
    subprocess.check_output(
        "grep -w VERSION_ID= /etc/os-release | awk -F\\\" '{print $2}' | cut -d '.' -f1",
        shell=True,
        text=True,
    )
    .strip()
)

audit_content_version = f"/home/ubuntu/auditDownyVibez"
audit_content_dir = os.path.join(AUDIT_CONTENT_LOCATION, audit_content_version)
audit_vars = f"vars/{BENCHMARK}.yml"

# Set output format variable
format = os.environ.get("FORMAT", "json")

# Set autogroup variable
auto_group = os.environ.get("GROUP", "ungrouped")

# Set default variable for varfile_path
VARS_PATH = os.environ.get("VARS_PATH")
if not VARS_PATH:
    varfile_path = os.path.join(audit_content_dir, audit_vars)
else:
    if os.path.isfile(VARS_PATH):
        varfile_path = VARS_PATH
    else:
        print(f"Passed option '-v' {VARS_PATH} does not exist")
        exit(1)

# Collect system variables for metadata
try:
    with open("/sys/class/dmi/id/product_uuid", "r") as uuid_file:
        host_machine_uuid = uuid_file.read().strip()
except FileNotFoundError:
    host_machine_uuid = subprocess.check_output(
        "dmidecode -s system-uuid", shell=True, text=True
    ).strip()

host_epoch = int(time.time())
host_os_locale = time.strftime("%Z")
host_os_name = subprocess.check_output(
    '''grep "^NAME=" /etc/os-release | cut -d '"' -f2 | sed 's/ //' | cut -d ' ' -f1''',
    shell=True,
    text=True,
).strip()
host_os_version = subprocess.check_output(
    '''grep "^VERSION_ID=" /etc/os-release | cut -d '"' -f2''',
    shell=True,
    text=True,
).strip()
host_os_hostname = subprocess.check_output("hostname", shell=True, text=True).strip()
# Set variable audit_out
OUTFILE = os.environ.get("OUTFILE")
html_filename = 'html_report_'
if not OUTFILE:
    audit_out = os.path.join(
        AUDIT_CONTENT_LOCATION, f"{html_filename}{host_os_hostname}.html"
    )
   
else:
    audit_out = OUTFILE
    
# Set the AUDIT json string
audit_json_vars = json.dumps(
    {
        "benchmark_type": BENCHMARK,
        "benchmark_os": BENCHMARK_OS,
        "benchmark_version": BENCHMARK_VER,
        "machine_uuid": host_machine_uuid,
        "epoch": host_epoch,
        "os_locale": host_os_locale,
        "os_release": host_os_version,
        "os_distribution": host_os_name,
        "os_hostname": host_os_hostname,
        "auto_group": auto_group,
        "system_type": host_system_type,
    }
)

# Run pre checks

print("\n## Pre-Checks Start\n")

FAILURE = 0
if os.path.exists(AUDIT_BIN) and os.path.getsize(AUDIT_BIN) > 0:
    print(f"OK Audit binary {AUDIT_BIN} is available")
else:
    print(f"WARNING - The audit binary is not available at {AUDIT_BIN}")
    FAILURE = 1

audit_file_path = os.path.join(audit_content_dir, AUDIT_FILE)
if os.path.isfile(audit_file_path):
    print(f"OK {audit_file_path} is available")
    
else:
    print(f"WARNING - the {audit_file_path} is not available")
    FAILURE = 2

if FAILURE != 0:
    print("## Pre-checks failed please see output")
    exit(1)
else:
    print("\n## Pre-checks Successful\n")

# Format output
output_summary = f"tail -2 {audit_out}"
format_output = f"-f {format}"

if format == "json":
    format_output = "-f json -o pretty"
    #output_summary = f"grep -A 4 \"summary\": {audit_out}"
    output_summary = f"{audit_out}"
elif format == "junit" or format == "tap":
    output_summary = ""

# Run commands
print("#############")
print("Audit Started")
print("#############")
print()

audit_command = f"{AUDIT_BIN} -g {audit_file_path} --vars {varfile_path} --vars-inline '{audit_json_vars}' v {format_output}"
subprocess.run(audit_command, shell=True, text=True, stdout=open(audit_out, "w"))

#JSON to HTML conversion function
def jsontoHtml(filename):
    with open(filename) as f:
        data = json.load(f)

    summary = data['summary']
    unique_titles = set()
    for test in data['results']:
        title = test['title']
        split_title = title.split("|", 1)
        id = split_title[0].strip() if len(split_title) == 2 else "N/A"
        test['id'] = id
    sorted_data = sorted(data['results'], key=lambda x: x['id'])

    dir = '/home/ubuntu/'
    filename = 'html_report_' + str(host_os_hostname) + '.html'
    outputhtml = dir + filename
    with open(outputhtml, 'w') as f:
        # Write the HTML header
        f.write("""<html>
        <head>
        <title>Test Results</title>
        <style>
        /* Styles for the top bar */
        .top-bar {{
            background-color: #333;
            color: white;
            padding: 10px;
            text-align: center;
        }}
        .top-bar h1 {{
            margin: 0;
        }}

        /* Styles for the summary container */
        .summary-container {{
            background-color: #eee;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin: 10px;
            text-align: center;
        }}
        .summary-container p {{
            margin-top: 0;
            font-size: 18px;
            font-weight: bold;
        }}
        .summary-container ul {{
            list-style-type: none;
            margin: 0;
            padding: 0;
            display: inline-block;
        }}
        .summary-container li {{
            display: inline-block;
            margin-right: 20px;
            font-size: 16px;
        }}

        /* Styles for the test results table */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }}

        th, td {{
            border: 1px solid #ddd;
            text-align: left;
            padding: 8px;
        }}

        th {{
            background-color: #333;
            color: white;
        }}
    </style>
        </head>
        <body>
            <div class="top-bar">
                <h1>auditDownyVibez</h1>
            </div>
            <div class="summary-container">
                <p>Summary:</p>
                <ul>
                    <li>Total tests: {0}</li>
                    <li>Failed tests: {1}</li>
                    <li>Duration: {2:.2f}s</li>
                </ul>
            </div>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Test Description</th>
                    <th>Test Result</th>
                </tr>
                """.format(summary['test-count'], summary['failed-count'], summary['total-duration'] / 1e9))

        for test in sorted_data:
            title = test['title']
            result = test['result']
            if title not in unique_titles:
                split_title = title.split("|", 1)
                id = test['id']
                test_description = split_title[1].strip() if len(split_title) == 2 else split_title[0].strip()

                if result == 1:
                    result_text = '<span style="color:green;">Passed</span>'
                elif result == 0:
                    result_text = '<span style="color:red;">Failed</span>'

                f.write(f"""<tr>
                    <td>{id}</td>
                    <td>{test_description}</td>
                    <td>{result_text}</td>
                    </tr>""")
                unique_titles.add(title)

        # Write the HTML table footer and HTML footer
        f.write("""
            </table>
        </body>
        </html>""")

# Create screen output
if (
    int(
        subprocess.run(
            f"grep -c {BENCHMARK} {audit_out}",
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
    )
    != 0
) or format == "junit" or format == "tap" or format == "json":
    output_summary_result = subprocess.run(
        output_summary, shell=True, text=True, stdout=subprocess.PIPE
    )
    if output_summary_result.returncode == 1:
        print(
            f"Summary here\n{output_summary_result.stdout.strip()}\nCompleted file located at {audit_out}"
        )
    else:
        print(f"HTML Report can be found at {audit_out}")
        print("###############")
        print("Audit Completed")
        print(audit_out)

        directory, filename = os.path.split(audit_out)
        jsontoHtml('/home/ubuntu/' + filename)

    

else:
    print(f"Failed Audit - Issues at:  {audit_out}")
