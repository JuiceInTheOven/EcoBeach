using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using WebApi.Logic.Entities;

namespace WebApi.Logic.Helpers
{
    public class FileManager
    {
        const string SEED_FILE = @"c:\Users\Guli\Documents\SwimSafe\src\WebApi\bin\Debug\net5.0\DK_BW2020.csv";

        public List<Beach> ReadFile()
        {
            ValidatePath(SEED_FILE);
            var data = new List<Beach>();
            
            using(StreamReader sr = new StreamReader(SEED_FILE))
            {
                // Skip header
                sr.ReadLine();
                int idx = 0;

                while (!sr.EndOfStream)
                {
                    var line = sr.ReadLine().Split('\t');

                    double longitude;
                    double latitude;
                    double.TryParse(line[6], out longitude);
                    double.TryParse(line[7], out latitude);

                    data.Add(new Beach
                    {
                        Id = ++idx,
                        CountryCode = line[0],
                        BathingWaterIdentifier = line[1],
                        GroupIdentifier = line[2],
                        Name = line[3],
                        ZoneType = line[4],
                        GeographicalConstraint = Boolean.Parse(line[5]),
                        Longitude = longitude,
                        Latitude = latitude,
                        ProfileURL = line[8],
                        Quality90 = line[9],
                        Quality91 = line[10],
                        Quality92 = line[11],
                        Quality93 = line[12],
                        Quality94 = line[13],
                        Quality95 = line[14],
                        Quality96 = line[15],
                        Quality97 = line[16],
                        Quality98 = line[17],
                        Quality99 = line[18],
                        Quality00 = line[19],
                        Quality01 = line[20],
                        Quality02 = line[21],
                        Quality03 = line[22],
                        Quality04 = line[23],
                        Quality05 = line[24],
                        Quality06 = line[25],
                        Quality07 = line[26],
                        Quality08 = line[27],
                        Quality09 = line[28],
                        Quality10 = line[29],
                        Quality11 = line[30],
                        Quality12 = line[31],
                        Quality13 = line[32],
                        Quality14 = line[33],
                        Quality15 = line[34],
                        Quality16 = line[35],
                        Quality17 = line[36],
                        Quality18 = line[37],
                        Quality19 = line[40],
                        Quality20 = line[43]
                    });
                }
            }
            return data;
        }

        private void ValidatePath(string path)
        {
            string codeBase = Assembly.GetExecutingAssembly().CodeBase;
            UriBuilder uri = new UriBuilder(codeBase);
            string assembly = Uri.UnescapeDataString(uri.Path);
            Path.GetDirectoryName(assembly);
            if (!File.Exists(path))
            {
                throw new FileNotFoundException("File does not exist!");
            }

            var info = new FileInfo(path);

            if (info.Extension != ".csv")
            {
                throw new FormatException("Invalid file extension!");
            }
        }
    }
}
