from comnet.downloader.downloader import main as download 
from comnet.parser.parser import main as parse
from comnet.normalizer.normalizer import main as normalize
from comnet.visualizer.visualizer import main as visualize

def main():
    download()
    parse()
    normalize()
    visualize()

if __name__ == "__main__":
    main()