document.addEventListener('DOMContentLoaded', function() {
	const eliminarLinks = document.querySelectorAll('.eliminar');
	eliminarLinks.forEach(function(link) {
		link.addEventListener('click', function(event) {
			if (!confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
				event.preventDefault();
			}
		});
	});
});
