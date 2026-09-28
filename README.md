# MeTube - Configuration Docker

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://github.com/alexta69/metube)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-2026.08.19-green)](https://github.com/yt-dlp/yt-dlp)

Interface web auto-hébergée pour [yt-dlp](https://github.com/yt-dlp/yt-dlp) — téléchargez des vidéos, audios et sous-titres depuis YouTube et des centaines d'autres sites.

## Démarrage rapide

```bash
git clone https://github.com/herold/metube-config.git
cd metube-config
docker compose up -d
```

Ouvrir http://localhost:8082 dans le navigateur.

## Structure

```
metube-config/
├── docker-compose.yml
├── .gitignore
├── README.md
├── config/
│   ├── ytdl-options.json          # Options globales yt-dlp
│   └── ytdl-options-presets.json  # 10 presets réutilisables
├── downloads/                     # Dossier de téléchargement
└── plugins/
    └── yt_dlp_plugins/
        └── postprocessor/
            ├── replaygain.py      # Tags ReplayGain
            └── srtfixer.py        # Correction sous-titres
```

## Configuration par défaut

| Option | Valeur | Description |
|--------|--------|-------------|
| **Langue audio** | Français | Priorise l'audio FR si disponible |
| **Sous-titres** | FR + EN | Auto-générés inclus |
| **Qualité** | 720p | H.264/MP4 pour compatibilité |
| **Simultanés** | 2 | Téléchargements en parallèle |
| **Reprise** | 3 | Tentatives sur fragments |
| **Port** | 8082 | Interface web |
| **Thème** | Sombre | Auto/dark/light configurable |

## Permissions (sans sudo)

Les fichiers sont créés en `664` (rw-rw-r--) pour modification/suppression libre:

```bash
# Le conteneur tourne en tant que 1000:1000
# Les fichiers sont accessibles en écriture
chmod -R 775 downloads/  # Si besoin
```

## Presets disponibles

Dans l'UI: **Advanced Options > Option Presets**

| Preset | Description |
|--------|-------------|
| `720p-francais` | Vidéo 720p, audio FR, sous-titres FR |
| `1080p-francais` | Vidéo 1080p, audio FR, sous-titres FR |
| `audio-mp3-francais` | Extraction MP3, priorité FR |
| `audio-flac-francais` | Extraction FLAC lossless, priorité FR |
| `audio-mp3` | Extraction MP3, meilleure qualité |
| `audio-flac` | Extraction FLAC lossless |
| `best-quality` | Meilleure qualité dispo, audio FR |
| `mobile-360p` | 360p mobile, audio FR |
| `no-subs` | Sans sous-titres |
| `subtitles-only` | Uniquement les sous-titres FR/EN |

### Sélection de langue audio

Les presets `-francais` utilisent:
- `ba[lang=fr]` — Préfère l'audio en français
- `formatsort: ["lang:fr"]` — Trie avec FR en priorité
- Fallback automatique si FR indisponible

## Plugins installés

### ReplayGain (`replaygain.py`)
Applique les tags ReplayGain pour un volume constant.

### SRT Fixer (`srtfixer.py`)  
Corrige les lignes dupliquées dans les sous-titres auto-générés YouTube.

### Plugins communautaires

Voir la [liste des plugins](https://github.com/yt-dlp/yt-dlp/wiki/Plugins):
- [Return Youtube Dislikes](https://github.com/pukkandan/yt-dlp-returnyoutubedislike) - Compteur de dislikes
- [DeArrow](https://github.com/QuantumWarpCode/yt-dlp-dearrow) - Titres sans clickbait

## SponsorBlock (intégré)

Activer dans `config/ytdl-options.json`:

```json
{
  "postprocessors": [
    {"key": "SponsorBlock", "categories": ["sponsor", "intro", "outro", "selfpromo"]},
    {"key": "ModifyChapters"}
  ]
}
```

## Personnalisation

### Modifier les options globales

Éditer `config/ytdl-options.json`:
```bash
docker compose restart
```

### Ajouter un preset

Éditer `config/ytdl-options-presets.json` — rechargé automatiquement.

### Ajouter un plugin

Créer dans `plugins/yt_dlp_plugins/postprocessor/` ou `extractor/`:
```python
from yt_dlp.postprocessor.common import PostProcessor

class MonPlugin(PostProcessor):
    def run(self, info):
        # Votre logique ici
        return [], info
```

## Mise à jour

```bash
docker compose pull
docker compose up -d
```

## Dépannage

```bash
# Vérifier les logs
docker logs metube -f

# Tester yt-dlp directement
docker exec -it metube yt-dlp --verbose "URL"

# Vérifier les plugins
docker exec metube python -c "import yt_dlp_plugins; print('OK')"
```

## Liens

- [MeTube GitHub](https://github.com/alexta69/metube)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [Plugins yt-dlp](https://github.com/yt-dlp/yt-dlp/wiki/Plugins)
- [Wiki MeTube](https://github.com/alexta69/metube/wiki)

## License

MIT
