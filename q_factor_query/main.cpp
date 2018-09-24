#include <bits/stdc++.h>
using namespace std;
typedef pair<int, int> ii;
const int N = 1024;

char buffer[N];
vector<string> juniper_ip;
const string folder = "/home/gardusi/q_factor/";
const string _stdout = folder + "stdout";
const string _stderr = folder + "stderr";
const string snmpwalk = "/usr/bin/snmpwalk -v 2c -c V01prO2005 ";
FILE *log_file = fopen((folder + "log.txt").c_str(), "w");

vector<string> run_command (const string command) {
	vector<string> command_output;
	system((command + " 1>" + _stdout + " 2>" + _stderr).c_str());
	FILE *output_file = fopen(_stdout.c_str(), "r");
	if (!output_file)
		exit(!fprintf(log_file, "[line %d] Failed to execute \"fopen output\"\n", __LINE__));
	while (fgets(buffer, N, output_file))
		buffer[strlen(buffer) - 1] = '\0',
		command_output.push_back(string(buffer));
	fclose(output_file), system((string("rm ") + _stdout).c_str()), system((string("rm ") + _stderr).c_str());
	return command_output;
}

void build_juniper_database () {
	vector<string> database = run_command((string("cat ") + folder + "database.txt").c_str());
	for (string i : database) {
		vector<string> fping = run_command((string("/usr/local/sbin/fping -a -g ") + i).c_str());
		for (string j : fping) {
			vector<string> check = run_command((snmpwalk + j + " sysDescr.0").c_str());
			for (string k : check) {
				if (k.find("Juniper") != string::npos) {
					juniper_ip.push_back(j);
					break;
				}
			}
		}
	}
}

string get_date () {
	return run_command(string("date \"+%d/%m/%Y\""))[0];
}

string get_ip_hostname (const string ip) {
	string ans = run_command(snmpwalk + ip + " sysName.0")[0];
	return ans.substr(32, int(ans.size()) - 32);
}

string get_interface_hostname (const string ip, const string interface) {
	string ans = run_command(snmpwalk + ip + " ifAlias." + interface)[0];
	return ans.substr(27 + int(interface.size()), int(ans.size()) - 27 - int(interface.size()));
}

string get_interface_name (const string ip, const string interface) {
	string ans = run_command(snmpwalk + ip + " ifDescr." + interface)[0];
	return ans.substr(27 + int(interface.size()), int(ans.size()) - 27 - int(interface.size()));
}

vector< pair<int, pair<string, string> > > get_interfaces (const string ip) {
	vector< pair<int, pair<string, string> > > interfaces;
	vector<string> output = run_command(snmpwalk + ip + " .1.3.6.1.4.1.2636.3.73.1.3.3.1.1.3");
	for (string s : output) {
		string interface = s.substr(45, int(s.size()) - 45);
		if (interface[0] != '.')
			continue;
		int interface_number, qfactor;
		sscanf(interface.c_str(), ".%d = INTEGER: %d", &interface_number, &qfactor);
		if (qfactor <= 0)
			continue;
		string interface_hostname = get_interface_hostname(ip, to_string(interface_number));
		if (interface_hostname.find("TRUNK") == string::npos)
			continue;
		string interface_name = get_interface_name(ip, to_string(interface_number));
		interfaces.push_back(make_pair(qfactor, make_pair(interface_name, interface_hostname)));
	}
	return interfaces;
}

int main () {
	build_juniper_database();
	const string date = get_date();
	FILE *file = fopen((folder + "file.txt").c_str(), "w");
	fprintf(file, "date;hostname;interface;description;qfactor\n");
	for (string ip : juniper_ip) {
		vector< pair<int, pair<string, string> > > interfaces = get_interfaces(ip);
		if (!int(interfaces.size()))
			continue;
		string ip_hostname = get_ip_hostname(ip);
		for (auto interface : interfaces)
			fprintf(file, "%s;%s;%s;%s;%.1lf\n", date.c_str(), ip_hostname.c_str(), interface.second.first.c_str(), interface.second.second.c_str(), double(interface.first) / 10.0);
	}
	fclose(file);
	return 0;
};