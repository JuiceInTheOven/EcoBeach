using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using WebApi.Logic.Models;

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

                while (!sr.EndOfStream)
                {
                    var line = sr.ReadLine().Split('\t');

                    double longitude;
                    double latitude;
                    double.TryParse(line[6], out longitude);
                    double.TryParse(line[7], out latitude);

                    data.Add(new Beach
                    {
                        
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
