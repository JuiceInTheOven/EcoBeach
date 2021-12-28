using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace WebApi.Logic.Models
{
    public class Beach : Entity
    {
        public string countryCode { get; set; }
        public string locationName { get; set; }
        public GeoLocation geoPosition { get; set; }
        public string date { get; set; }
        public int land_squareMeters { get; set; }
        public double land_percentage { get; set; }
        public int water_squareMeters { get; set; }
        public double water_percentage { get; set; }

    }

    public class GeoLocation
    {
        public double lat { get; set; }
        public double lon { get; set; }
    }
}
