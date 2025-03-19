#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Video to Audio Converter
------------------------
Un outil simple pour extraire l'audio des fichiers vidéo.
Utilise FFmpeg comme moteur de conversion.
"""

import os
import sys
import argparse
import subprocess
import glob
from pathlib import Path
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def check_ffmpeg():
    """Vérifie si FFmpeg est installé sur le système."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.error("FFmpeg n'est pas installé ou n'est pas dans le PATH.")
        logger.error("Veuillez installer FFmpeg: https://ffmpeg.org/download.html")
        return False

def convert_video_to_audio(input_path, output_path, audio_format='mp3', quality='192k', verbose=False):
    """
    Convertit un fichier vidéo en fichier audio.
    
    Args:
        input_path (str): Chemin vers le fichier vidéo d'entrée
        output_path (str): Chemin vers le fichier audio de sortie
        audio_format (str): Format de sortie (mp3, wav, etc.)
        quality (str): Qualité audio (128k, 192k, 256k, 320k)
        verbose (bool): Mode verbeux
    
    Returns:
        bool: True si la conversion est réussie, False sinon
    """
    if not os.path.exists(input_path):
        logger.error(f"Le fichier d'entrée n'existe pas: {input_path}")
        return False
    
    # S'assurer que le dossier de sortie existe
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    # Préparer les options FFmpeg
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vn"  # Supprime la piste vidéo
    ]
    
    # Ajouter les options en fonction du format
    if audio_format == 'mp3':
        ffmpeg_cmd.extend([
            "-c:a", "libmp3lame",
            "-b:a", quality
        ])
    elif audio_format == 'wav':
        ffmpeg_cmd.extend([
            "-c:a", "pcm_s16le"
        ])
    else:
        ffmpeg_cmd.extend([
            "-c:a", "copy"  # Essayer de copier le codec audio tel quel
        ])
    
    # Ajouter le fichier de sortie
    ffmpeg_cmd.append(output_path)
    
    # Exécuter la commande
    try:
        if verbose:
            logger.info(f"Exécution de la commande: {' '.join(ffmpeg_cmd)}")
            result = subprocess.run(ffmpeg_cmd, check=True)
        else:
            result = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
        
        logger.info(f"Conversion réussie: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
        return True
    
    except subprocess.CalledProcessError as e:
        logger.error(f"Erreur lors de la conversion: {e}")
        if verbose and e.stderr:
            logger.error(f"Détails: {e.stderr.decode('utf-8', errors='replace')}")
        return False

def batch_convert(input_dir, output_dir, audio_format='mp3', quality='192k', verbose=False):
    """
    Convertit tous les fichiers vidéo d'un dossier en fichiers audio.
    
    Args:
        input_dir (str): Chemin du dossier contenant les vidéos
        output_dir (str): Chemin du dossier où sauvegarder les fichiers audio
        audio_format (str): Format de sortie audio
        quality (str): Qualité audio
        verbose (bool): Mode verbeux
    
    Returns:
        tuple: (nombre de succès, nombre d'échecs)
    """
    # S'assurer que les chemins se terminent par un séparateur
    input_dir = os.path.join(input_dir, '')
    output_dir = os.path.join(output_dir, '')
    
    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    # Extensions vidéo courantes
    video_extensions = ('*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv', '*.webm')
    
    # Trouver tous les fichiers vidéo
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(input_dir, ext)))
        # Ajout des extensions en majuscules
        video_files.extend(glob.glob(os.path.join(input_dir, ext.upper())))
    
    if not video_files:
        logger.warning(f"Aucun fichier vidéo trouvé dans {input_dir}")
        return 0, 0
    
    logger.info(f"Démarrage de la conversion par lots: {len(video_files)} fichiers trouvés")
    
    success_count = 0
    failure_count = 0
    
    for video_file in video_files:
        # Remplacer l'extension par le format audio souhaité
        base_name = os.path.basename(video_file)
        output_name = os.path.splitext(base_name)[0] + f".{audio_format}"
        output_path = os.path.join(output_dir, output_name)
        
        if convert_video_to_audio(video_file, output_path, audio_format, quality, verbose):
            success_count += 1
        else:
            failure_count += 1
    
    logger.info(f"Conversion par lots terminée. Succès: {success_count}, Échecs: {failure_count}")
    return success_count, failure_count

def parse_arguments():
    """Parse les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Convertisseur Vidéo en Audio - Extrait l'audio de fichiers vidéo.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-i", "--input", 
        required=True,
        help="Chemin vers le fichier vidéo ou le dossier (en mode batch)"
    )
    
    parser.add_argument(
        "-o", "--output", 
        required=True,
        help="Chemin de sortie pour le fichier audio ou le dossier (en mode batch)"
    )
    
    parser.add_argument(
        "-f", "--format", 
        choices=["mp3", "wav"], 
        default="mp3",
        help="Format de sortie audio"
    )
    
    parser.add_argument(
        "-q", "--quality", 
        choices=["128k", "192k", "256k", "320k"], 
        default="192k",
        help="Qualité audio (pour MP3)"
    )
    
    parser.add_argument(
        "-b", "--batch", 
        action="store_true", 
        help="Active le mode de traitement par lots"
    )
    
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Active le mode verbeux pour plus de détails"
    )
    
    return parser.parse_args()

def main():
    """Fonction principale du programme."""
    # Vérifier si FFmpeg est installé
    if not check_ffmpeg():
        sys.exit(1)
    
    # Lire les arguments
    args = parse_arguments()
    
    # Configurer le niveau de log en fonction du mode verbeux
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Exécuter la conversion
    if args.batch:
        if not os.path.isdir(args.input):
            logger.error(f"Le chemin d'entrée doit être un dossier en mode batch: {args.input}")
            sys.exit(1)
        
        success, failure = batch_convert(
            args.input, 
            args.output, 
            args.format,
            args.quality,
            args.verbose
        )
        
        # Afficher un résumé
        logger.info(f"Résumé: {success} fichiers convertis avec succès, {failure} échecs")
        if failure > 0:
            sys.exit(1)
    else:
        # Conversion d'un seul fichier
        if not os.path.isfile(args.input):
            logger.error(f"Le fichier d'entrée n'existe pas: {args.input}")
            sys.exit(1)
        
        success = convert_video_to_audio(
            args.input, 
            args.output, 
            args.format,
            args.quality,
            args.verbose
        )
        
        if not success:
            sys.exit(1)
    
    logger.info("Conversion terminée avec succès!")

if __name__ == "__main__":
    main()
