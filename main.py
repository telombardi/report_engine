import logging
from config import Config
from pydoc import locate
import colorama
from colorama import Fore, Back, Style
import argparse
from pathlib import Path

def main():
  '''load configuration file'''
  try:
    cfg = Config()
  except JSONDecodeError as jde:
    print(jde)
    print('config.json is not parseable.')
    exit()

  '''Start logging functions'''
  logfile = Path(cfg.config['log_location'] + '/' + cfg.config['log_prefix'] + '.log')
  logging.basicConfig(filename=logfile, level=cfg.config['log_level'])
  logging.info('/n===Reporting Engine Starts===')
  logging.info(cfg.config)
  
  '''Define argument parser'''
  parser = argparse.ArgumentParser(prog=cfg.config['program_name'],description=cfg.config['program_description'],epilog=cfg.config['program_epilog'])
  parser.add_argument('report')
  parser.add_argument('output')
  args = parser.parse_args()
  
  '''Load specific report module'''
  report_module = locate(args.report)
  my_output = Path(args.output)
  report_class = getattr(report_module,'Report')
  report = report_class(my_output)
  report.run()
  
if __name__ == "__main__":
  main()
