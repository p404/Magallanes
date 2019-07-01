#!/usr/bin/env python3
import config
from common.utils import logger
from containers.api import magallanes_init

def main():
    logger('info', 'Starting Magallanes')
    magallanes_init()

if __name__ == "__main__":
    main()