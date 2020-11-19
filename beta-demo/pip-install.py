import ray
import argparse


import subprocess
from subprocess import CalledProcessError


@ray.remote
def func(pkg):
    print("installing {}".format(pkg))
    try:
        subprocess.check_call(["pip", "install", pkg])
    except CalledProcessError:
        print("Failed to install package: {}".format(pkg))
        return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "packages", nargs="*", help="packages to install on the session"
    )
    ray.init()
    # ray.worker.global_worker.run_function_on_all_workers()

    args = parser.parse_args()
    print(args.packages)
    for pkg in args.packages:
        installs = ray.get(
            [func.remote(pkg) for x in range(int(ray.available_resources()["CPU"]))]
        )

        assert False not in installs
