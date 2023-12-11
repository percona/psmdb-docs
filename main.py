import re

def define_env(env):
  "Hook function"

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