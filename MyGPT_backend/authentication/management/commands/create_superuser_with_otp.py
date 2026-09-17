import getpass

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django_otp.plugins.otp_totp.models import TOTPDevice

from ...otp_utils import render_terminal_qr


class Command(BaseCommand):
    help = 'Create a superuser and enroll it with TOTP authentication in one step.'

    def add_arguments(self, parser):
        parser.add_argument('--username', dest='username')
        parser.add_argument('--email', dest='email')

    def handle(self, *args, **options):
        user_model = get_user_model()

        username = options.get('username') or input('Username: ').strip()
        email = options.get('email') or input('Email address: ').strip()
        password = self._prompt_password()

        if user_model.objects.filter(username=username).exists():
            raise CommandError(f'A user named "{username}" already exists.')

        user = user_model.objects.create_superuser(username=username, email=email, password=password)

        device, _ = TOTPDevice.objects.get_or_create(
            user=user,
            name='admin-authenticator',
            defaults={'confirmed': False},
        )

        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
        self.stdout.write('Scan this QR code with an authenticator app:')
        self.stdout.write(render_terminal_qr(device.config_url))
        token = input('Enter the current six-digit code to confirm enrollment: ').strip()

        if not device.verify_token(token):
            device.delete()
            raise CommandError('Invalid authentication code; the superuser was created but TOTP was not enrolled. Re-run "setup_admin_otp" to try again.')

        device.confirmed = True
        device.save(update_fields=['confirmed'])
        self.stdout.write(self.style.SUCCESS('TOTP authentication is enabled for this administrator.'))

    def _prompt_password(self):
        while True:
            password = getpass.getpass('Password: ')
            password_confirm = getpass.getpass('Password (again): ')
            if password != password_confirm:
                self.stderr.write('Passwords do not match, please try again.')
                continue
            try:
                validate_password(password)
            except ValidationError as error:
                self.stderr.write('\n'.join(error.messages))
                continue
            return password
