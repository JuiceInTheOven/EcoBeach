using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using WebApi.DataAccess.Context;
using WebApi.Logic.Models;

namespace WebApi.DataAccess.Services
{
    public class BeachService
    {
        private readonly IMongoCollection<Beach> _beaches;

        public BeachService(IBeachDatabaseSettings settings)
        {
            string connectionString = Environment.GetEnvironmentVariable("EcoConnectionString");
            string databaseName = Environment.GetEnvironmentVariable("EcoDatabaseName");
            string collectionName = Environment.GetEnvironmentVariable("EcoCollectionName");

            var client = new MongoClient(connectionString);
            var database = client.GetDatabase(databaseName);
            _beaches = database.GetCollection<Beach>(collectionName);
        }

        public List<Beach> Get() =>
            _beaches.Find(beach => true).ToList();

        public Beach Get(string id) =>
            _beaches.Find<Beach>(beach => beach._id == id).FirstOrDefault();

        public Beach Create(Beach beach)
        {
            _beaches.InsertOne(beach);
            return beach;
        }

        public void Update(string id, Beach beachIn) =>
            _beaches.ReplaceOne(beach => beach._id == id, beachIn);

        public void Remove(Beach beachIn) =>
            _beaches.DeleteOne(beach => beach._id == beachIn._id);

        public void Remove(string id) =>
            _beaches.DeleteOne(beach => beach._id == id);
    }
}
