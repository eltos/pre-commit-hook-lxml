from __future__ import annotations

import argparse
from lxml import etree
from editorconfig import get_properties, EditorConfigError
import logging

INDENT = 2
RETRIES = 5

def pretty_print(filename: str, space: str, width: int) -> None:
  parser = etree.XMLParser(remove_blank_text=True)
  tree = etree.XML(filename, parser=parser).getroottree()
  etree.indent(tree, space=width * space)
  return etree.tostring(tree,
                        pretty_print=True,
                        encoding=parse.docinfo.encoding,
                        xml_declaration=True)

def beautify(filename: str, width: int, retries: int) -> None:
  space = ' '
  try:
    properties = get_properties(filename)
    tab = properties['indent_style']
    if tab == 'tab':
      width = 1
      space = '\t'
    else:
      width = int(properties['indent_size'])
      space = ' '
    logging.debug(f'Indentation set to {indent_size} via editorconfig')
  except EditorConfigError:
    pass

  with open(filename, 'r') as f:
    content = f.read()

  original = content
  for _ in range(retries):
    xml = pretty_print(original, space=space, width=width)
    if xml == original:
      break
    original = xml

  if xml == content:
    logging.debug(f'No change: {filename}')
  else:
    logging.info(f'Formatted: {filename}')
    with open(filename, "wb") as f:
      f.write(xml)

def main(argv: Sequence[str] | None = None) -> int:
  argv = argv if argv is not None else sys.argv[1:]
  parser = argparse.ArgumentParser(prog='lxml_format', description='Prettyprint XML file with lxml')

  parser.add_argument(
    '-i', '--indent',
    dest='width',
    type=int,
    default=INDENT,
    help='Number of spaces to use for indentation when no .editorconfig found. Default: %(default)s)'
  )

  parser.add_argument(
    '-r', '--retries',
    dest='retries',
    type=int,
    default=RETRIES,
    help='Max number of retries to reach content stabilisation. Default: %(default)s)'
  )

  parser.add_argument(
    '-l', '--log-level', '--log',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    dest='loglevel',
    default='INFO',
    help='Debug level.'
  )


  parser.add_argument(
    'filenames',
    nargs='*',
    help='Files to format'
  )

  args = parser.parse_args(argv)

  try:
    for filename in args.filenames:
      beautify(filename, args.width, args.retries)
    return 0
  except Exception as e:
    logging.error(e)
    return 1

if __name__ == '__main__':
  raise SystemExit(main())
