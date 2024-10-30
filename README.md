# `pre-commit` hook to reformat XML files

This project implements a [pre-commit] [hook] to [gently](#example) reformat XML
files using the [tostring] function of the [lxml] project.

+ Ensure the tree is properly indented, one tag per line
+ Pick indentation settings from [editorconfig], whenever available. Settings
  are mapped as best as possible to the capabilities of the [tostring] function,
  i.e. either a number of spaces, or indent using tabs.
+ Clean up spacing in tags
+ Automatically rewrite as self-closing tags
+ Add an extra space at the end of self-closing tags -- for extra readability
  (optional)
+ Automatically use the same/change line endings
+ Preserve spacing in tags content
+ Keep comments
+ Remove blank lines
+ Enforce an XML declaration (by default) and control/detect its quoting style

  [pre-commit]: https://pre-commit.com/
  [hook]: ./.pre-commit-hooks.yaml
  [tostring]: https://lxml.de/api/lxml.etree-module.html#tostring
  [lxml]: https://lxml.de/
  [editorconfig]: https://editorconfig.org/

## Usage

Add the following to your `.pre-commit-config.yaml` file. The default is to
automatically reformat all files of [type] `xml`. You might want to check the
latest version of the repository [here] and change the rev key.

Note: The `rev` is NOT the version of [lxml] to run, but rather the version of
the hook, i.e. a release of this project.

```yaml
  - repo: https://github.com/efrecon/pre-commit-hook-lxml
    rev: v0.1.4
    hooks:
      - id: format-xml
```

  [type]: https://pre-commit.com/#filtering-files-with-types
  [here]: https://github.com/efrecon/pre-commit-hook-lxml/releases

If your project does not use [editorconfig], you can still enforce indentation
for all files through the `--indent` CLI option/hook argument. This can also be
used to override [editorconfig] settings. For example, the following would
enforce 3 spaces of indentation for all XML file, independently of your
[editorconfig] settings or if there are no settings:

```yaml
  - repo: https://github.com/efrecon/pre-commit-hook-lxml
    rev: v0.1.4
    hooks:
      - id: format-xml
        args:
          - --indent=3
```

The pre-commit hook can be controlled using a number of environment
[variables](#environment-variables), all starting with
`PRE_COMMIT_HOOK_LXML_FORMAT_` and a number of [options](#cli-options):

+ Use options to change the behaviour for all users of your repository, e.g.
  specifying the indentation. Options can be specified under the `args` key in
  the YAML configuration.
+ Use environment variables to adapt to your local client-side requirements,
  e.g. turning up logging to understand possible problems.

### CLI Options

The CLI options can be used from the YAML pre-commit configuration, using the
`args` key. The recognised options are:

+ `-i` or `--indent` is the number of spaces to use when indenting files.
  Indentation can be set to `0` to not indent the file. When the value of this
  option is strictly negative, the hook will pick [editorconfig] settings, if
  possible. In case of problems, a default of `2` will be used.
+ `-r` or `--retries` is the maximum number of times that indentation is run on
  the file before it does not change. This is because lxml may need to run
  several times due to inconsistencies. The (good?) default is `5` and there are
  little reasons to deviate from it.
+ `-e` or `--endings` (or `--line-endings`) controls the line endings of the
  reformatted files. It can take one of the following values.
  - `unix` for LF line endings.
  - `windows` for CRLF line endings.
  - `mac` for CR line endings (Mac Classic).
  - `auto` (the default) will detect the line endings of the original file and
    apply it to the reformatted file. If the file had mixed line endings, the
    same line endings will be applied to the entire file in this order:
    `windows` > `mac` > `unix` -- as soon as the original file had one CRLF
    line ending, all lines will end with CRLF, etc.
+ `-s` or `--self-closing` controls if there should be an additional space just
  before the `/>` characters in self-closing tags. Possible values are:
  - `space`: a space is always added, for all self-closing tags. This is the
    default. See [example](#example).
  - `nospace`: no extra space will be added, this the LXML default.
  - `auto`: a space will be added if the file contained the ` />` sequence of
    characters.
+ `-d` or `--declaration` controls if there should be a declaration, and its
  quoting style. Possible values are:
  - A negative boolean, e.g. `off`, `false`, `no`, etc. to turn off generating
    an XML declaration at the top of the files.
  - `double-quotes` to enforce the use of double quotes in the XML declaration.
  - `single-quotes` to enforce the use of single quotes in the XML declaration.
  - `auto` to detect quoting style from the rest of the XML content and apply it
    to the XML declaration. This uses a crude heuristic and prefers double
    quotes.
+ `-l` or `--log-level` is the log level. One of `DEBUG`, `INFO`, `WARNING`,
  `ERROR` or `CRITICAL`.
+ `-w` or `--write` tells the hook implementation to write the changes to the
  files. This is automatically turned on from the
  [default](./.pre-commit-hooks.yaml) `args`.

### Environment Variables

Environment variables match the long options as follows. When an environment
variable is set, its value will prevail over the value of the command-line
option. This is because the hook is meant to be used from a YAML specification
that is checked in your repository. Environment variables provide a way to
depart from centralised options to adapt to local installation "quirks".

+ `PRE_COMMIT_HOOK_LXML_FORMAT_INDENT` is the same as `--indent`.
+ `PRE_COMMIT_HOOK_LXML_FORMAT_RETRIES` is the same as `--retries`.
+ `PRE_COMMIT_HOOK_LXML_FORMAT_WRITE` is the same as `--write`. It recognises
  boolean values such as `on`, `True`, `FALSE`, `t` or `0`.
+ `PRE_COMMIT_HOOK_LXML_FORMAT_LOG_LEVEL` is the same as `--log-level`.
+ `PRE_COMMIT_HOOK_LXML_LINE_ENDINGS` is the same as `--line-endings`.
+ `PRE_COMMIT_HOOK_LXML_SELF_CLOSING` is the same as `--self-closing`.
+ `PRE_COMMIT_HOOK_LXML_DECLARATION` is the same as `--declaration`.

## Example

The following example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<test><inside>text</inside>
<long>    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</long>
<space  > </space    >
<attr attr0="short" attr1="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud" attr2="exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"/>
                        <attrext attr0="osdifjsdfoi" attr2="oooddddddddddddd">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud</attrext>
                <empty></empty>
</test>
```

would be reformatted to the following, provided an indentation of `2` spaces:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<test>
  <inside>text</inside>
  <level>
    <one />
    <two>
      <more />
    </two>
  </level>
  <long>    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</long>
  <space> </space>
  <attr attr0="short" attr1="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud" attr2="exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum" />
  <attrext attr0="osdifjsdfoi" attr2="oooddddddddddddd">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud</attrext>
  <empty />
</test>
```

Note that:

+ the `<inside>` tag has been moved to a separate line.
+ the `<level>` tree is broken into several lines, and indented with `2` spaces
  at each level.
+ spacing in the `<space>` tag has been cleaned up, but its content preserved.
+ the `<empty>` tag has been replaced by a self-closing tag.
+ the `<empty />` self-closing tag has an extra space before the closing `/>`
+ the XML declaration uses double-quotes since attributes use double-quotes in
  the reformatted output.

## Development

When developing the `pre-commit` hook, you can test it using the
[`try-repo`][try-repo] sub-command. You can temporarily specify arguments using
the [`args`][hook-args] key in the [YAML](./.pre-commit-hooks.yaml)
configuration of this hook. In order to be able to see the loggers output, you
will need to run with the `--verbose` flag to the `try-repo` sub-command.

  [try-repo]: https://pre-commit.com/#pre-commit-try-repo
  [hook-args]: https://pre-commit.com/#hooks-args

## Known Limitations

When files were not properly formatted, e.g. when not run with the `--write`
flag, the implementation returns an error code that is related to the number of
files that had errors. The code is the number of erroneous files + `2`, in order
to avoid using [standard] error codes. Since error codes are interpreted modulo
`256`, this means that it is **possible** for this hook to pass while there are
problems. However, this is an edge case, especially since the default running
scenario (and goal!) is to reformat the files.

  [standard]: https://tldp.org/LDP/abs/html/exitcodes.html
