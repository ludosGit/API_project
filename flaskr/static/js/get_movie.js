// Function to get movie data from the API using the URL params
async function fetchMovieDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const title = urlParams.get('title');

    try {
        const response = await fetch(`/mymovies/title/${title}`);
        
        if (response.ok) {
            const movies = await response.json();
            const allViewDates = movies.flatMap(movie => movie.view_date || []);
            const sortedMovies = movies
                .flatMap(movie => movie.view_date ? [{ ...movie }] : []) // Ensure view_date exists
                .sort((a, b) => b.view_date.localeCompare(a.view_date)); // Sort in descending order
            if (sortedMovies.length === 0) {
                document.getElementById('movie-details').innerHTML = '<p class="error-message">No valid view dates found.</p>';
                return;
            }
            const latestMovie = sortedMovies[0];

            const firstImage = sortedMovies.find(movie => movie.image)?.image || '';
            
            const movieDetailsHtml = `
                <div class="movie-container">
                    <h2>${latestMovie.title}</h2>
                    <p><strong>Genre:</strong> ${latestMovie.genre}</p>
                    <p><strong>Rating:</strong> ${latestMovie.rating}</p>
                    <p><strong>Director:</strong> ${latestMovie.director}</p>
                    <p><strong>Year:</strong> ${latestMovie.year}</p>
                    <p><strong>Comment:</strong> ${latestMovie.comment}</p>
                    <p><strong>Views:</strong>  ${allViewDates.join(", ")}</p>
                    <img src="${firstImage}" alt="${latestMovie.title} Image" />
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