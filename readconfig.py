import pkg_resources
import sys

def main():
    print("in main")
    config = pkg_resources.resource_string(__name__, 'config/ayyanar.conf')
    print((config))

main()