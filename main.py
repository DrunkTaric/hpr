from fileinput import filename
import os
import api
import modules

def extract(path):
    recs = modules.main(path)
    recs.start_process()
    size = api.letter_size_calculate(recs)
    return {
        "path": path,
        "preasure": api.pen_pressure_calculate(recs),
        "angle":  api.baseline_angle_calculate(recs),
        "Lsize": size,
        "margin": api.top_margin_calculate(recs, size),
        "distance": api.distance_calculate(recs)
    }

def main():
    Logger = modules.log("main")
    if not os.path.exists("./dataset"): Logger.write('error', 'Cannot find Dataset directory'); quit()
    folders = [f for f in os.listdir('./dataset')]
    if len(folders) < 1: Logger.write('warning', 'The Dataset directory is empty'); quit()
    print(Logger.Color(255, 0, 0, "Made by "), 'Anas Abdulatif')
    with open('output.txt', 'w+') as dani:
        for folder in folders:
            files = [f for f in os.listdir(f'./dataset/{folder}')]
            for FileName in files:
                Data = extract('./{0}/{1}/{2}'.format("dataset", folder, FileName))
                Logger.write('debug', "Image = "+ FileName)
                Logger.write('debug', "Pen Presure = "+ str(Data['preasure']))
                Logger.write('debug', "Baseline Angle = "+ str(Data['angle']))
                Logger.write('debug', "Letters Size = "+ str(Data['Lsize']))
                Logger.write('debug', "Top Margin = "+ str(Data['margin']))
                Logger.write('debug', "Distances = "+ str(Data['distance']))
                dani.write("{0},{1},{2},{3},{4},{5},{6} {7}".format(
                    Data['preasure'],
                    Data['angle'],
                    Data['Lsize'],
                    Data['margin'],
                    Data['distance'],
                    FileName,
                    folder, 
                    "\n"
                ))
                Logger.write("info", f"new line was written by identifier = {folder}/{FileName}")
        Logger.write("info", "All photos are done")
    

if __name__ == "__main__":
    main()