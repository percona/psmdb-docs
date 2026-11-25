import re
from pathlib import Path

def define_env(env):
  "Hook function"

  @env.macro
  def render_snippet(filename, start=1, end=None):
      """Expand variables in a snippet before Markdown processes it."""
      path = Path(__file__).parent / 'snippets' / filename
      lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
      return env.env.from_string(''.join(lines[start - 1:end])).render(**env.variables)

  @env.macro
  def k8spxcjira(bugnumber):
      return '[K8SPXC-'+str(bugnumber)+'](https://jira.percona.com/browse/K8SPXC-'+str(bugnumber)+')'
  @env.macro
  def cloudjira(bugnumber):
      return '[CLOUD-'+str(bugnumber)+'](https://jira.percona.com/browse/CLOUD-'+str(bugnumber)+')'
  @env.macro
  def optionlink(optionname, optionprefix=''):
      linkname=optionname.replace('.', '-').lower()
      linkname=re.sub('&lt;.*?&gt;-', '', linkname)
      if (optionprefix != ''):
        optionprefix+='-'
      return '<a name=\"'+optionprefix+linkname+'\"></a> ['+optionname+'](#'+optionprefix+linkname+')'
