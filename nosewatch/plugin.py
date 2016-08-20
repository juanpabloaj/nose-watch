import sys
from nose.plugins import Plugin
from subprocess import Popen


class WatchPlugin(Plugin):
    """
    Plugin that use watchdog for continuous tests run.
    """
    name = 'watch'
    is_watching = False
    sys = sys

    def call(self, args):
        Popen(args).wait()

    def finalize(self, result):
        argv = list(self.sys.argv)
        argv.remove('--with-watch')

        clear_command = 'clear'
        if sys.platform == 'win32':
            clear_command = 'cls'

        watchcmd = clear_command + ' && ' + ' '.join(argv)
        call_args = ['watchmedo', 'shell-command', '-c',
            watchcmd, '-R', '-p', '*.py', '.']
        try:
            self.call(call_args)
        except KeyboardInterrupt:
            self.sys.stdout.write('\nStopped\n')

