// Function to get movie data from the API using the URL params
async function fetchMovieDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const director = urlParams.get('director');
    const title = urlParams.get('title');

    if (!director || !title) {
        document.getElementById('movie-details').innerHTML = '<p class="error-message">Please provide both director and title in the URL.</p>';
        return;
    }

    try {
        const response = await fetch(`/mymovies/directors/${director}/${title}`);
        
        if (response.ok) {
            const movie = await response.json();
            
            const movieDetailsHtml = `
                <div class="movie-container">
                    <h2>${movie.title}</h2>
                    <p><strong>Genre:</strong> ${movie.genre}</p>
                    <p><strong>Rating:</strong> ${movie.rating}</p>
                    <p><strong>Director:</strong> ${movie.director}</p>
                    <p><strong>Year:</strong> ${movie.year}</p>
                    <p><strong>Comment:</strong> ${movie.comment}</p>
                    <p><strong>Views:</strong> ${movie.views.join(", ")}</p>
                    <img src="${movie.image}" alt="${movie.title} Image" />
                </div>
            `;
            document.getElementById('movie-details').innerHTML = movieDetailsHtml;
        } else {
            const error = await response.json();
            document.getElementById('movie-details').innerHTML = `<p class="error-message">${error.error}</p>`;
        }
    } catch (error) {
        document.getElementById('movie-details').innerHTML = `<p class="error-message">An error occurred while fetching the movie details.</p>`;
    }
}

// Fetch the movie details when the page loads
fetchMovieDetails();