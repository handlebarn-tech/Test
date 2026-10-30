using System.Linq;
using NUnit.Framework;

namespace Dispo.Domain.Tests
{
    public class DomainAssemblyTests
    {
        [Test]
        public void DomainAssembly_HasNoUnityReferences()
        {
            var assembly = typeof(DomainAssembly).Assembly;
            Assert.AreEqual(DomainAssembly.Name, assembly.GetName().Name);
            var unityRefs = assembly.GetReferencedAssemblies().Where(a => a.Name.StartsWith("Unity")).Select(a => a.Name);
            CollectionAssert.IsEmpty(unityRefs);
        }
    }
}
