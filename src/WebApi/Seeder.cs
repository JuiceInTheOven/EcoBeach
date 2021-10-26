using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using WebApi.DataAccess.Context;
using WebApi.Logic.Helpers;

namespace WebApi
{
    public static class Seeder
    {
        public static void Initialize(BeachContext context)
        {
            FileManager fm = new FileManager();
            var data = fm.ReadFile();
            context.Beaches.AddRange(data);
            try
            {
                context.SaveChanges();
            }
            catch(Exception e)
            {

            }
        }
    }
}
