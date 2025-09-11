# Contributing to tubearchivist as a developer

## Developement Environment
As outlined in the [CONTRIBUTING.md](https://github.com/bmcdonough/tubearchivist/blob/master/CONTRIBUTING.md)

### Native
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python backend/manage.py runserver
```

### Docker
Edit the docker-compose.yml file and replace `image: bbilly1/tubearchivist` line with `build: .`
```bash
docker compose up --build
```

### Remote
- This assumes a standard Ubuntu Server VM with docker and docker compose already installed.
- Configure your local DNS to resolve tubearchivist.local to the IP of the VM.
```bash
./deploy.sh test
```

## Adding a new configuration element

- frontend/src/pages/SettingsApplication.tsx

- frontend/src/stores/AppSettingsStore.ts

- frontend/src/api/loader/loadAppsettingsConfig.ts

- backend/appsettings/src/config.py

- backend/appsettings/serializers.py