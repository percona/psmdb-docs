# Virtual hardware recommendations for cloud deployments

Percona Server for MongoDB runs reliably on cloud infrastructure and is supported for all cloud providers. 

This document includes virtual hardware recommendations for the most popular cloud providers.

## Amazon Web Services (AWS)

Percona recommends the AWS EC2 memory-optimized instances as they best suit Percona Server for MongoDB usage. The `R7i` offers the best performance-per-dollar ratio among all memory-optimized AWS EC2 instance types. The cost efficiency makes these instances a strong choice for organizations that need high and cost-efficient performance. You can review the Amazon website for more details on [Amazon EC2 R5 Instances :octicons-link-external-16:](https://aws.amazon.com/ec2/instance-types/r7i/).

| Instance size | vCPU | Memory (GiB) |
|---|---|---|
| r7i.xlarge | 4 | 32 |
| r7i.2xlarge | 8 | 64 |
| r7i.4xlarge| 16 | 128 |
| r7i.8xlarge| 32 | 256 |
| r7i.16xlarge| 64 | 512 |

The recommendation is based on Yahoo! Cloud Serving Benchmark (YCSB) version 0.17.0 and is fully described in the article "[Which memory-optimized AWS EC2 instance type is best for MongoDB? :octicons-link-external-16:](https://community.intel.com/t5/Blogs/Tech-Innovation/Cloud/Which-memory-optimized-AWS-EC2-instance-type-is-best-for-MongoDB/post/1615010)"

## Microsoft Azure

Percona recommends Virtual Machine (VM) sizes from the D-series for Percona Server for MongoDB deployments in Microsoft Azure. `Dsv5` instance family is the most cost-efficient choice. For more information on Azure Virtual Machines, see [Linux Virtual Machines pricing :octicons-link-external-16:](https://azure.microsoft.com/en-gb/pricing/details/virtual-machines/linux/).

| Instance size | vCPU | Memory (GiB) |
|---|---|---|
| D8s v5 | 8 | 32 |
| D16s v5 | 16 | 64 |
| D32s v5 | 32 | 128 |
| D64s v5 | 64 | 256 |
| D96s v5 | 96 | 384 |

The recommendation is based on Yahoo! Cloud Serving Benchmark (YCSB) version 0.17.0 and fully described in the article "[Best Virtual Machine Size for Self-Managed MongoDB on Microsoft Azure :octicons-link-external-16:](https://community.intel.com/t5/Blogs/Tech-Innovation/Cloud/Best-Virtual-Machine-Size-for-Self-Managed-MongoDB-on-Microsoft/post/1606921)"

## Google Cloud

Percona recommends `c3-standard` machine families among other general-purpose GCP instances for Percona Server for MongoDB deployment in Google Cloud Platform (GCP). For more information on Google virtual machines, see [Google Compute Products :octicons-link-external-16:](https://cloud.google.com/compute/vm-instance-pricing?hl=en).

| Instance size | vCPU | Memory (GiB) |
|---|---|---|
| c3-standard-8 | 8 | 32 |
| c3-standard-22 | 16 | 88 |
| c3-standard-44 | 32 | 176 |
| c3-standard-88 | 64 | 352 |

The recommendation is based on Yahoo! Cloud Serving Benchmark (YCSB) version 0.17.0 and fully described in the article "[MongoDB: Best choice of instance type on GCP :octicons-link-external-16:](https://community.intel.com/t5/Blogs/Tech-Innovation/Cloud/MongoDB-Best-choice-of-instance-type-on-GCP/post/1556443)"
