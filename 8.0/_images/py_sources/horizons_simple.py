from diagrams import Diagram, Cluster, Edge
from diagrams.aws.general import Client
from diagrams.onprem.compute import Server
from diagrams.aws.network import NLB
from diagrams.aws.general import GenericDatabase

with Diagram("Horizons workflow", show=False, filename="mongodb_horizons_diagram"):
    # External World
    external_client = Client("MongoDB Client")

    with Cluster("Virtual Private Cloud (VPC)"):
            nlb = NLB("Load Balancer\nmongo.external.mycompany.com")
            with Cluster("MongoDB Replica Set"):
                # Create nodes in horizontal alignment
                primary = GenericDatabase("Primary\npsmdb1.internal.net")
                secondary1 = GenericDatabase("Secondary\npsmdb2.internal.net")
                secondary2 = GenericDatabase("Secondary\npsmdb3.internal.net")

            app_server = Server("Internal app\n10.0.1.100")

    # External client flow
    external_client >> Edge(label="4. Routes Reply") >>  nlb
    nlb >> Edge(label="1. SNI: mongo.external.mycompany.com") >> external_client

    nlb >> Edge(label="2. Forwards to Primary") >> primary
    primary >> Edge(label="3. Horizons reply: external hostnames" ) >>  nlb
    

    # Internal app flow - positioned to avoid overlap with cluster label
    app_server >> Edge(label="1 - Internal DNS (SNI: psmdb1.internal.net)") >> primary
    primary >> Edge(label="2 - Internal Reply (internal hostnames)") >> app_server
    
    # Position these connections to avoid label overlap
    app_server >> Edge(label="Connects directly\nto other nodes") >> secondary1
    app_server >> Edge(label="Connects directly\nto other nodes") >> secondary2

    # Replica set replication - arranged to avoid crossing
    primary << Edge(color="blue", style="dashed") >> secondary1
    secondary1 << Edge(color="blue", style="dashed") >> secondary2
    secondary2 << Edge(color="blue", style="dashed") >> primary
