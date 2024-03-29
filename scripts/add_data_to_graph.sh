#!/bin/bash
#
# ARG_HELP([Upload JSONLD and Turtle data to a Neurobagel graph])
# ARG_POSITIONAL_SINGLE([dir],[Path to directory containing .jsonld and/or .ttl files. ALL .jsonld and .ttl files in this directory will be uploaded.])
# ARG_POSITIONAL_SINGLE([graph-url],[Host and port at which to access the graph database to add data to (e.g., localhost:7200)])
# ARG_POSITIONAL_SINGLE([graph-database],[Name of graph database to add data to])
# ARG_POSITIONAL_SINGLE([user],[Username for graph database access])
# ARG_POSITIONAL_SINGLE([password],[Password for graph database user])
# ARG_OPTIONAL_BOOLEAN([clear-data],[],[Whether or not to first clear all existing data from the graph database],[off])
# ARG_OPTIONAL_BOOLEAN([use-stardog-syntax],[],[Set to use Stardog API endpoints to update the specified graph database. If unset, assumes the graph database is a GraphDB database.],[off])
# ARG_OPTIONAL_BOOLEAN([log-output],[],[Whether or not to write the output to a log file],[off])
# ARG_OPTIONAL_SINGLE([log-file],[],[Path to the log file],[LOG.txt])
# ARGBASH_GO()
# needed because of Argbash --> m4_ignore([
### START OF CODE GENERATED BY Argbash v2.9.0 one line above ###
# Argbash is a bash code generator used to get arguments parsing right.
# Argbash is FREE SOFTWARE, see https://argbash.io for more info
# Generated online by https://argbash.io/generate


die()
{
	local _ret="${2:-1}"
	test "${_PRINT_HELP:-no}" = yes && print_help >&2
	echo "$1" >&2
	exit "${_ret}"
}


begins_with_short_option()
{
	local first_option all_short_options='h'
	first_option="${1:0:1}"
	test "$all_short_options" = "${all_short_options/$first_option/}" && return 1 || return 0
}

# THE DEFAULTS INITIALIZATION - POSITIONALS
_positionals=()
# THE DEFAULTS INITIALIZATION - OPTIONALS
_arg_clear_data="off"
_arg_use_stardog_syntax="off"

_arg_log_output="off"
_arg_log_file="LOG.txt"

print_help()
{
	printf '%s\n' "Upload JSONLD and Turtle data to a Neurobagel graph"
	printf 'Usage: %s [-h|--help] [--(no-)clear-data] [--(no-)use-stardog-syntax] [--(no-)log-output] [--log-file <arg>] <dir> <graph-url> <graph-database> <user> <password>\n' "$0"
	printf '\t%s\n' "<dir>: Path to directory containing .jsonld and/or .ttl files. ALL .jsonld and .ttl files in this directory will be uploaded."
	printf '\t%s\n' "<graph-url>: Host and port at which to access the graph database to add data to (e.g., localhost:7200)"
	printf '\t%s\n' "<graph-database>: Name of graph database to add data to"
	printf '\t%s\n' "<user>: Username for graph database access"
	printf '\t%s\n' "<password>: Password for graph database user"
	printf '\t%s\n' "-h, --help: Prints help"
	printf '\t%s\n' "--clear-data, --no-clear-data: Whether or not to first clear all existing data from the graph database (off by default)"
	printf '\t%s\n' "--use-stardog-syntax, --no-use-stardog-syntax: Set to use Stardog API endpoints to update the specified graph database. If unset, assumes the graph database is a GraphDB database. (off by default)"
  	printf '\t%s\n' "--log-output, --no-log-output: Whether or not to write the output to a log file (off by default)"
    printf '\t%s\n' "--log-file: Path to the log file (default: 'LOG.txt')"
}


parse_commandline()
{
	_positionals_count=0
	while test $# -gt 0
	do
		_key="$1"
		case "$_key" in
			-h|--help)
				print_help
				exit 0
				;;
			-h*)
				print_help
				exit 0
				;;
			--no-clear-data|--clear-data)
				_arg_clear_data="on"
				test "${1:0:5}" = "--no-" && _arg_clear_data="off"
				;;
			--no-use-stardog-syntax|--use-stardog-syntax)
				_arg_use_stardog_syntax="on"
				test "${1:0:5}" = "--no-" && _arg_use_stardog_syntax="off"
				;;
			--no-log-output|--log-output)
				_arg_log_output="on"
				test "${1:0:5}" = "--no-" && _arg_log_output="off"
				;;
			--log-file)
				test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
				_arg_log_file="$2"
				shift
				;;
			--log-file=*)
				_arg_log_file="${_key##--log-file=}"
				;;
			*)
				_last_positional="$1"
				_positionals+=("$_last_positional")
				_positionals_count=$((_positionals_count + 1))
				;;
		esac
		shift
	done
}


handle_passed_args_count()
{
	local _required_args_string="'dir', 'graph-url', 'graph-database', 'user' and 'password'"
	test "${_positionals_count}" -ge 5 || _PRINT_HELP=yes die "FATAL ERROR: Not enough positional arguments - we require exactly 5 (namely: $_required_args_string), but got only ${_positionals_count}." 1
	test "${_positionals_count}" -le 5 || _PRINT_HELP=yes die "FATAL ERROR: There were spurious positional arguments --- we expect exactly 5 (namely: $_required_args_string), but got ${_positionals_count} (the last one was: '${_last_positional}')." 1
}


assign_positional_args()
{
	local _positional_name _shift_for=$1
	_positional_names="_arg_dir _arg_graph_url _arg_graph_database _arg_user _arg_password "

	shift "$_shift_for"
	for _positional_name in ${_positional_names}
	do
		test $# -gt 0 || break
		eval "$_positional_name=\${1}" || die "Error during argument parsing, possibly an Argbash bug." 1
		shift
	done
}

parse_commandline "$@"
handle_passed_args_count
assign_positional_args 1 "${_positionals[@]}"

# OTHER STUFF GENERATED BY Argbash

### END OF CODE GENERATED BY Argbash (sortof) ### ])
# [ <-- needed because of Argbash


# Reassign positional args to more readable named variables (https://argbash.readthedocs.io/en/latest/guide.html#using-parsing-results)
jsonld_dir=$_arg_dir
user=$_arg_user
password=$_arg_password
graph_db=$_arg_graph_database
graph_url=$_arg_graph_url
clear_data=$_arg_clear_data  # value is either on or off (https://argbash.readthedocs.io/en/stable/guide.html#optional-arguments)
use_stardog_syntax=$_arg_use_stardog_syntax

log_output=$_arg_log_output
log_file=$_arg_log_file

DELETE_TRIPLES_QUERY="
DELETE {
	?s ?p ?o .
} WHERE {
	?s ?p ?o .
}"

# Depending on the graph backend used, set URLs for uploading data to and clearing data in graph database
base_url="http://${graph_url}/${graph_db}"
if [ "$use_stardog_syntax" = "on" ]; then
	upload_data_url=$base_url
	clear_data_url="${base_url}/update"
else
	upload_data_url="${base_url}/statements"
	clear_data_url=$upload_data_url
fi

# Main logic
main() {
    # Clear existing data in graph database if requested
    if [ "$clear_data" = "on" ]; then
        echo -e "\nCLEARING EXISTING DATA FROM ${graph_db}..."

        response=$(curl -u "${user}:${password}" -s -S -i -w "\n%{http_code}\n" \
            -X POST $clear_data_url \
            -H "Content-Type: application/sparql-update" \
            --data-binary "${DELETE_TRIPLES_QUERY}")

        # Extract and check status code outputted as final line of response
        httpcode=$(tail -n1 <<< "$response")
        if (( $httpcode < 200 || $httpcode >= 300 )); then
            echo -e "\nERROR: Failed to clear ${graph_db}:"
            echo "$(sed '$d' <<< "$response")"
            echo -e "\nEXITING..."
            exit 1
        fi
    fi

    # Add data to specified graph database
    echo -e "\nUPLOADING DATA FROM ${jsonld_dir} TO ${graph_db}...\n"

    upload_failed=()

    for db in ${jsonld_dir}/*.jsonld; do
        # Prevent edge case where no matching files are present in directory and so loop executes once with glob pattern string itself
        [ -e "$db" ] || continue

        echo "$(basename ${db}):"
        response=$(curl -u "${user}:${password}" -s -S -i -w "\n%{http_code}\n" \
                    -X POST $upload_data_url \
                    -H "Content-Type: application/ld+json" \
                    --data-binary @${db})

        httpcode=$(tail -n1 <<< "$response")
        if (( $httpcode < 200 || $httpcode >= 300 )); then
            upload_failed+=("${db}")
        fi
        # Print rest of response to stdout
        echo -e "$(sed '$d' <<< "$response")\n"
    done

    for file in ${jsonld_dir}/*.ttl; do
        [ -e "$file" ] || continue

        echo "$(basename ${file}):"
        response=$(curl -u "${user}:${password}" -s -S -i -w "\n%{http_code}\n" \
                    -X POST $upload_data_url \
                    -H "Content-Type: text/turtle" \
                    --data-binary @${file})

        httpcode=$(tail -n1 <<< "$response")
        if (( $httpcode < 200 || $httpcode >= 300 )); then
            upload_failed+=("${file}")
        fi
        echo -e "$(sed '$d' <<< "$response")\n"
    done

    echo "FINISHED UPLOADING DATA FROM ${jsonld_dir} TO ${graph_db}."

    if (( ${#upload_failed[@]} != 0 )); then
        echo -e "\nERROR: Upload failed for these files:"
        printf '%s\n' "${upload_failed[@]}"
    fi
}

# Call the main logic function with or without output redirection
if [ "$log_output" = "on" ]; then
    main > "$log_file"
else
    main
fi
# ] <-- needed because of Argbash