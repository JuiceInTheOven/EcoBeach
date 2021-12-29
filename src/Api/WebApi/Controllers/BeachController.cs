using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using WebApi.Logic.Models;
using WebApi.DataAccess.Context;
using Microsoft.EntityFrameworkCore;
using WebApi.DataAccess.Services;

namespace WebApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BeachController : ControllerBase
    {
        private readonly BeachService service;
        public BeachController(BeachService service)
        {
            this.service = service;
        }

        [HttpGet]
        public ActionResult<List<Beach>> Get() => service.Get();

        [HttpGet("{id:length(24)}", Name = "GetBeach")]
        public ActionResult<Beach> Get(string id)
        {
            var beach = service.Get(id);

            if (beach == null)
            {
                return NotFound();
            }

            return beach;
        }

        [HttpPost]
        public ActionResult<Beach> Create(Beach beach)
        {
            service.Create(beach);

            return CreatedAtRoute("GetBook", new { id = beach._id.ToString() }, beach);
        }

        [HttpPut("{id:length(24)}")]
        public IActionResult Update(string id, Beach bookIn)
        {
            var beach = service.Get(id);

            if (beach == null)
            {
                return NotFound();
            }

            service.Update(id, bookIn);

            return NoContent();
        }

        [HttpDelete("{id:length(24)}")]
        public IActionResult Delete(string id)
        {
            var beach = service.Get(id);

            if (beach == null)
            {
                return NotFound();
            }

            service.Remove(beach._id);

            return NoContent();
        }
    }
}
