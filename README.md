# Convertisseur Vidéo en Audio

Un outil simple et efficace pour extraire l'audio de vos fichiers vidéo.

## Fonctionnalités

- Convertit des fichiers vidéo (MP4, AVI, MOV, etc.) en fichiers audio (MP3, WAV)
- Supporte le traitement par lots de plusieurs fichiers
- Interface en ligne de commande simple à utiliser
- Option pour ajuster la qualité audio de sortie

## Prérequis

- Python 3.7 ou supérieur
- FFmpeg installé sur votre système

## Installation

1. Clonez ce dépôt sur votre machine :
```
git clone https://github.com/YohannQMR/video-to-audio-converter.git
cd video-to-audio-converter
```

2. Installez les dépendances requises :
```
pip install -r requirements.txt
```

3. Assurez-vous que FFmpeg est installé sur votre système :
   - **Windows** : [Téléchargez FFmpeg](https://ffmpeg.org/download.html#build-windows) et ajoutez-le à votre PATH
   - **macOS** : `brew install ffmpeg`
   - **Linux** : `sudo apt-get install ffmpeg` ou équivalent pour votre distribution

## Utilisation

### Conversion simple

```
python video2audio.py -i chemin/vers/video.mp4 -o chemin/vers/sortie.mp3
```

### Conversion par lots

```
python video2audio.py -i dossier/videos/ -o dossier/audios/ --batch
```

### Options disponibles

- `-i`, `--input` : Chemin vers le fichier vidéo ou le dossier (en mode batch)
- `-o`, `--output` : Chemin de sortie pour le fichier audio ou le dossier (en mode batch)
- `-f`, `--format` : Format de sortie audio (mp3, wav), par défaut : mp3
- `-q`, `--quality` : Qualité audio (128k, 192k, 256k, 320k), par défaut : 192k
- `-b`, `--batch` : Active le mode de traitement par lots
- `-v`, `--verbose` : Active le mode verbeux pour plus de détails pendant la conversion

## Exemples

1. Convertir une vidéo en MP3 avec qualité élevée :
```
python video2audio.py -i ma_video.mp4 -o mon_audio.mp3 -q 320k
```

2. Convertir toutes les vidéos d'un dossier en fichiers WAV :
```
python video2audio.py -i dossier/videos/ -o dossier/audios/ -f wav --batch
```

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
