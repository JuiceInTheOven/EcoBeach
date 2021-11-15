using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using WebApi.Logic.Entities;
using WebApi.DataAccess.Context;
using Microsoft.EntityFrameworkCore;

namespace WebApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BeachController : ControllerBase
    {
        private readonly BeachContext context;
        public BeachController(BeachContext context)
        {
            this.context = context;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<Beach>>> GetBeaches()
        {
            return await context.Beaches.Include(x => x.Name).ToListAsync();
        }

        // GET: BeachController/Details/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Beach>> GetBeach(int id)
        {
            var beach = await context.Beaches.FindAsync(id);
            if (beach == null)
            {
                return NotFound();
            }
            return beach;
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> PutBeach(int id, Beach beach)
        {
            if (id != beach.Id)
            {
                return BadRequest();
            }
            context.Entry(beach).State = EntityState.Modified;
            try
            {
                await context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!BeachExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }
            return NoContent();
        }

        [HttpPost]
        public async Task<ActionResult<Beach>> PostBeach(Beach beach)
        {
            context.Beaches.Add(beach);
            await context.SaveChangesAsync();
            return CreatedAtAction("GetBeach", new { id = beach.Id }, beach);
        }

        // POST: BeachController/Delete/5
        [HttpDelete("{id}")]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult<Beach>> DeleteBeach(int id)
        {
            var beach = await context.Beaches.FindAsync(id);
            if (beach == null)
            {
                return NotFound();
            }
            context.Beaches.Remove(beach);
            await context.SaveChangesAsync();
            return beach;
        }

        private bool BeachExists(int id)
        {
            return context.Beaches.Any(e => e.Id == id);
        }
    }
}
