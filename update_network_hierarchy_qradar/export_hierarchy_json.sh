SEC_TOKEN="380d1847-6713-49ca-d9cf-385394dbd460"
AUTH_HEADER="SEC: $SEC_TOKEN"
API_VERSION_HEADER="Version: 15.1" 
QRADAR_CONSOLE_IP="10.100.100.100"
OUTFILE="network_hiearchy_export.json"

curl -S -X GET \
-H "$API_VERSION_HEADER" \
-H "$AUTH_HEADER" \
-H 'Accept: application/json' \
--insecure "https://$QRADAR_CONSOLE_IP/api/config/network_hierarchy/staged_networks" > "$OUTFILE"