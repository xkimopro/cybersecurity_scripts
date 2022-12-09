
# QRadar Administration Commands

## Show Deployment Versioning
ssh in qradar console
```console
/opt/qradar/support/all_servers.sh -C -k /opt/qradar/bin/myver -v 
```

## Show Apps Running
ssh in qradar console
```console
psql -U qradar -c "select i.id,i.name,i.status,i.task_status,i.managed_host_id, m.hostname from installed_application_instance as i left join managedhost as m on m.id = i.managed_host_id;"
```


## QRadar Services

| Service | Purpose | Runs on | Impact |
| --- | --- | --- | --- |
| accumulator | Responsible for counting. In order to generate the time series graphs in the QRadar UI in a reasonable time, the accumulator creates by-minute, by-hour, and by-day counts of data within the system for quickly populating these time series graphs. | Console and Managed Hosts | Aggregate Data, Reports, Searches |
| arc_builder | Aggregates flows and events into bundles based on a set of known CIDR and service ports. | Console only | [Connection](https://www.ibm.com/docs/en/qsip/7.4?topic=overview-visualizing-network-connection-data) data for QRadar Risk Manager appliances. This service is only used by QRadar Risk Manager. |
| ariel\_proxy\_server | The ariel proxy server is responsible for proxying search requests from different processes to the various ariel query servers.  After the results are returned from the query servers, ariel proxy can transform and aggregate data into various orderings and store into server-side cursors for later processing and retrieval. | Console only | All requests to managed host for data from searches would stop until this service restarts. |
| ariel\_query\_server | Ariel query server is responsible for reading the ariel database on the Managed hosts and sends the data matching the request back to the proxy server for further processing. | Managed Hosts | All searches of the Ariel Database would stop on the managed hosts. |
| asset_profiler | Responsible for persisting the assets and identity models into the database. | Console only | Assets would not be added or updated until this service came back online. |
| docker | Docker is responsible for deploying and managing containerized applications. | Console and App Host | All applications stop working while the service is restarted. Also data collected by applications is lost during the restart. |
| ecs-ec-ingress | Event Correlation Service - Event Collector Ingress: collects the events in a buffer while ecs-ec and ecs-ep are being restarted. Then, it spools the data back to ecs-ec and ecs-ep | Console and Managed Hosts | This service when stopped would not allow events to be collected in a buffer and spooled to the other ecs services. |
| ecs-ec | Event Correlation Service - Event Collector: parse, normalize, and coalesce the events. | Console and Managed Hosts | Impacts Parsing and normalizing events and flows would stop |
| ecs-ep | Event Correlation Service - Event Processor: correlates events (Custom Rule Engine), stores events in the Ariel database and forwards events matching rules within CRE to the Magistrate component. | Console and Managed Hosts | Impacts Correlation. Parsing and event storage |
| ha_manager | Service responsible for distributed replicated block device (DRBD) control and starting or restarting other services. If store is mounted and VIP use. | Any Server in HA | Restarts all services including networking for the host in active HA status. Might affect Distribution Replication Block Device when restarted on a host with standby status. |
| historical\_correlation\_server | Provides abilities to create offense based on historical data. For example, Bulk loading data, one-time rule testing, and so on. | Console and Managed Hosts | Impacts historical searches on Offense data. |
| hostcontext | Runs on each appliance in a deployment. Runs the "ProcessManager" component that is responsible for starting, stopping, and verifying status for each component within the deployment. It is responsible for the packaging (console) and the download/apply (MH) of our DB replication bundles. Responsible for requesting, downloading, unpacking, and notifying other components within an appliance of updated configuration files. Responsible for monitoring postgresql transactions and restarting any process that exceeds the pre-determined time limit. This portion is referred to as "TxSentry". Responsible for disk maintenance routines for disk cleanup. Also, responsible for starting tunnels, ecs, accumulator, Ariel\_proxy, Ariel\_query, Qflow, reporting, Asset_profiler. | Console and Managed Hosts | Hostcontext is the manager for all the other services except ecs-ingress. All services controlled by hostcontext would be inactive until they restarted. |
| hostservices | Runs as an on-going daemon. It keeps track of 2 other running processes, Message Queues (IMQ), which opens up communication ports between QRadar Components and PostgreSQL. | Console and Managed Hosts | The database stops working as well as IMQ. This also impacts Hostcontext and Tomcat. |
| Network Services | The Network service restart as part of the QRadar patch pretest. | Console and Managed Hosts | Events might be interrupted as a result of the network services restarting. Console UI access and SSH might not be available until the network services restart. |
| qflow | Collects and 'creates' flow information from multiple sources. | Console and Managed Hosts | Flow data would not be available until restarted. |
| reporting_executor | Runs the scheduler for reporting. | Console only | All running reports would be canceled and would need to be restarted. New scheduled reports would not run until this service starts. |
| Tomcat | Web container used to hold our UI and webservices/RPC calls. | Console only | UI would not be available. |
| vis | The engine that drives scanner modules. | Console and Managed Hosts | Scans would not work and if scans are running would need to be restated. |

## QRadar Event Pipeline
![QRadar Event Pipeline](https://3.bp.blogspot.com/-N8hnpgJ58x4/WOMqppe9_4I/AAAAAAAABvk/M7FXSvpjzvAlLwP54ptzssbkjKOgOVQ7ACLcB/s640/Schermafbeelding%2B2017-04-04%2Bom%2B06.34.42.png)

## Test
