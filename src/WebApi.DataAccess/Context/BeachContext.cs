using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using WebApi.Logic.Entities;

namespace WebApi.DataAccess.Context
{
    public class BeachContext : DbContext
    {
        public virtual DbSet<Beach> Beaches { get; set; }

        public BeachContext(DbContextOptions<BeachContext> options) : base(options) { }

    }
    public class DesignTimeDbContextFactory : IDesignTimeDbContextFactory<BeachContext>
    {
        public BeachContext CreateDbContext(string[] args)
        {
            IConfigurationRoot configuration = new ConfigurationBuilder().SetBasePath(Directory.GetCurrentDirectory()).AddJsonFile(@Directory.GetCurrentDirectory() + "/../WebApi/appsettings.json").Build();
            var builder = new DbContextOptionsBuilder<BeachContext>();
            var connectionString = configuration.GetConnectionString("LocalDB");
            builder.UseSqlServer(connectionString);
            return new BeachContext(builder.Options);
        }
    }
}
