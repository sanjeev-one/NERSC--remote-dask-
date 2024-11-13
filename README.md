# Remote Dask Workflow on NERSC

This README provides instructions to set up and execute code remotely on a NERSC Dask cluster using a local machine. The workflow involves creating and managing a Dask cluster on NERSC, establishing a secure connection to access the Dask dashboard locally, and running distributed tasks using Dask. The steps outlined include prerequisites and instructions for configuring and running the main workflow script.

## Prerequisites

1. **Set Up SFAPI Client Keys**:
   - Go to the [NERSC Dashboard](https://my.nersc.gov/) and navigate to **Profile > Create an SF API Client Key**.
   - Enter the IP address of your local machine to authorize it.
   - Download the following files and save them locally:
     - `clientid.txt`
     - `private.pem`
   - Move these files to a `.superfacility` folder on your local machine (typically located at `~/.superfacility`, adjacent to the `.ssh` folder).

2. **Configure SSH Proxy for NERSC Tunnel**:
   - Run the `sshproxy.sh` script to set up SSH keys for the NERSC tunnel. This proxy will be valid for one day.
   - Ensure the SSH tunnel configuration is correct for the day you plan to run tasks.

3. **Modify `main.ipynb` with User Information**:
   - Open `main.ipynb` and update the notebook with your NERSC username and local paths to the downloaded keys.

## Workflow Overview

The `main.ipynb` notebook orchestrates the setup and management of a Dask cluster on a NERSC system through the SF API, providing the following capabilities:

1. **Starting a Dask Cluster on NERSC (via SLURM)**:
   - `main.ipynb` uses the SF API to allocate compute resources on NERSC and starts a Dask cluster on these nodes.
   
2. **Establishing an SSH Tunnel to Access Dask Dashboard**:
   - After launching the Dask cluster, the notebook sets up an SSH tunnel, allowing the local machine to access the Dask dashboard. 
   - The dashboard will be accessible at `localhost:8787`, and a local Dask client can connect to the cluster at `localhost:8786`.

3. **Running Dask Tasks from the Local Machine**:
   - Ensure you are using a local Dask version matching the NERSC Dask cluster version (currently `dask==2023.12.1`).
   - Once the cluster is set up, initiate the Dask client on your local machine as follows:

     ```python
     from dask.distributed import Client, progress
     
     client = Client('localhost:8786')
     client
     ```

4. **Monitoring Progress**:
   - The Dask dashboard at `localhost:8787` will provide a live view of tasks, resource usage, and other important cluster metrics.

