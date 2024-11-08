# scripts/download_bird_songs.py
import os
import argparse
import requests
import urllib.request
from pathlib import Path
from birdsong_classification.utils.path_utils import get_data_dir, get_models_dir, get_results_dir


def download_bird_songs(species, quality='A', page=1, num_files=150, start_index=1):#, output_dir='../data/raw'):
    """
    Download bird songs from xeno-canto.org
    
    Parameters:
        species (str): Bird species name (e.g., 'Eurasian blue tit')
        quality (str): Recording quality (default: 'A')
        page (int): Page number to start from (default: 1)
        num_files (int): Number of files to download (default: 150)
        start_index (int): Starting index for file naming (default: 1)
        output_dir (str): Directory to save files (default: '../data/raw')
    """
    # Sanitize species name for folder creation
    sanitized_species = "_".join(species.lower().split())
    
    # Create species-specific output directory
    species_output_path = get_data_dir() / "raw" / sanitized_species #Path(output_dir) / sanitized_species
    species_output_path.mkdir(parents=True, exist_ok=True)
    
    # Construct URL
    species_url = '%20'.join(species.split())
    url = f'https://xeno-canto.org/api/2/recordings?query={species_url}%20q:{quality}&page={page}'
    
    # Fetch data from API
    try:
        response = requests.get(url)  # Changed to GET
        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return
    
    # Check if there are enough recordings
    recordings = data.get("recordings", [])
    if len(recordings) < num_files:
        print(f"Only found {len(recordings)} recordings. Adjusting num_files to {len(recordings)}.")
        num_files = len(recordings)
    
    # Download files
    print(f"Downloading {num_files} recordings for {species}...")
    for i in range(num_files):
        try:
            filename = f"{start_index + i}.mp3"
            filepath = species_output_path / filename
            
            # Skip if file already exists
            if filepath.exists():
                print(f"File {filename} already exists, skipping...")
                continue
            
            # Download file
            file_url = recordings[i].get("file")
            if not file_url:
                print(f"No file URL for recording {i+1}, skipping...")
                continue
            
            urllib.request.urlretrieve(file_url, str(filepath))
            print(f"Downloaded file {i+1}/{num_files}: {filename}")
            
        except Exception as e:
            print(f"Error downloading file {i+1}: {e}")
            continue
    
    print("Download complete!")

def main():
    parser = argparse.ArgumentParser(description='Download bird songs from xeno-canto.org')
    parser.add_argument('--species', type=str, default='Eurasian blue tit,House sparrow,Common chaffinch',
                      help='Bird species name')
    parser.add_argument('--quality', type=str, default='A',
                      help='Recording quality (A-E)')
    parser.add_argument('--page', type=int, default=1,
                      help='Page number to start from')
    parser.add_argument('--num-files', type=int, default=300,
                      help='Number of files to download')
    parser.add_argument('--start-index', type=int, default=1,
                      help='Starting index for file naming')
    #parser.add_argument('--output-dir', type=str, 
    #                  default='../../../data/raw/',  
    #                  help='Directory to save files')
        
    args = parser.parse_args()
    
    for species in args.species.split(','):
        download_bird_songs(
            species=species,
            quality=args.quality,
            page=args.page,
            num_files=args.num_files,
            start_index=args.start_index,
            #output_dir=args.output_dir
        )

if __name__ == "__main__":
    main()
