#!/usr/bin/env python

import time
import asyncio
import logging

from os.path import join

from sfapi_client         import Client, AsyncClient
from sfapi_client.compute import Machine
from sfapi_client.jobs    import JobState

from sfapi_connector import KeyManager, OsSFAPI, OsWrapper, LOGGER


async def async_main():
    km = KeyManager()
    print(f"Loaded: {km.id=}, {km.key=}")

    # Get the user info, "Who does the api think I am?"
    async with AsyncClient(key=km.key) as client:
        user = await client.user()

    # Let's see what the user object has in it
    print(f"Client corresponds to {user=}")


def check_dir():
    km = KeyManager()
    target = "~/sfapi_test"

    with Client(key=km.key) as client:
        target = target.replace("~/", km.home)
        print(f"{km.home=}, {target=}")

        perlmutter = client.compute(Machine.perlmutter)
        print(perlmutter.status)

        perlmutter.run(f"mkdir -p {target}")
        [dir] = perlmutter.ls(target, directory=True)
        print(dir)


def check_open():
    target = "~/sfapi_test/test.txt"

    os = OsWrapper()

    with os.open(target, "w", mk_target_dir=False) as f:
        f.write("hi\n")
        f.write("ho\n")
        f.write("hum\n")

    with os.open(target, "rb") as f:
        lines = f.readlines()

    print(lines)


def check_stat():
    target = "~/sfapi_test/test.txt"

    os = OsWrapper()

    st = os.stat(target)
    print(st)


def check_mkdir():
    target = "~/sfapi_test/testdir4"

    os = OsWrapper()

    os.mkdir(target)


def check_chmod():
    target = "~/sfapi_test/testdir1"

    os = OsWrapper()

    os.chmod(target, 0o600)


def submit_job():
    N = 1000

    target = "~/sfapi_test"

    job_script = f"""#!/bin/bash
#SBATCH -q debug
#SBATCH -A lcls
#SBATCH -N 1
#SBATCH -C cpu
#SBATCH -t 00:01:00
#SBATCH -J sfapi-demo
#SBATCH --exclusive
#SBATCH --output={target}/sfapi-demo-%j.out
#SBATCH --error={target}/sfapi-demo-%j.error

module load python
# Prints N random numbers to form a normal disrobution
python -c "import numpy as np; numbers = np.random.normal(size={N}); [print(n) for n in numbers]"
    """ 

    os = OsWrapper()
    job_stript_path = join(target, "job_script.sh")

    with os.open(job_stript_path, "w", mk_target_dir=False) as f:
        f.write(job_script)

    km = KeyManager()
    with Client(key=km.key) as client:
        perlmutter = client.compute(Machine.perlmutter)
        [job_script_remote] = perlmutter.ls(
            job_stript_path.replace("~/", km.home), directory=False
        )

        print(f"Jobscript is at: {job_script_remote}")

        job = perlmutter.submit_job(job_script_remote)
        print(f"Submitted_job: {job.jobid}")

        while True:
            job.update()
            print(f"The job state is: {job.state} ({type(job.state)})")
            if job.state not in [JobState.PENDING, JobState.RUNNING, JobState.COMPLETING]:
                break
            time.sleep(10)


def check_exists():
    os = OsWrapper()
    print(os.path.exists("~/sfapi_test/does_not_exist.txt"))
    print(os.path.exists("~/sfapi_test/"))
    print(os.path.exists("~/sfapi_test/test.txt"))


if __name__ == "__main__":

    LOGGER.setLevel(logging.DEBUG)
    os = OsWrapper(backend=OsSFAPI())

    km = KeyManager()
    asyncio.run(async_main())
    # check_dir()
    # check_open()
    # check_mkdir()
    # check_stat()
    # check_chmod()
    # submit_job()
    check_exists()