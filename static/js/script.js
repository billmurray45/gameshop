document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded, initializing carousels...")

  // Featured Carousel
  const featuredCarousel = document.querySelector(".featured-carousel")
  if (featuredCarousel) {
    const featuredSlides = featuredCarousel.querySelectorAll(".carousel-slide")
    const featuredPrevBtn = featuredCarousel.querySelector(".carousel-arrow.prev")
    const featuredNextBtn = featuredCarousel.querySelector(".carousel-arrow.next")
    let featuredCurrentSlide = 0

    console.log("Featured carousel elements:", {
      slides: featuredSlides.length,
      prevBtn: !!featuredPrevBtn,
      nextBtn: !!featuredNextBtn,
    })

    function showFeaturedSlide(index) {
      featuredSlides.forEach((slide) => slide.classList.remove("active"))

      // Handle index bounds
      if (index < 0) index = featuredSlides.length - 1
      if (index >= featuredSlides.length) index = 0

      featuredCurrentSlide = index
      if (featuredSlides[featuredCurrentSlide]) {
        featuredSlides[featuredCurrentSlide].classList.add("active")
      }
      console.log("Showing featured slide:", featuredCurrentSlide)
    }

    // Initialize first slide
    showFeaturedSlide(0)

    // Event listeners for featured carousel
    if (featuredPrevBtn) {
      featuredPrevBtn.addEventListener("click", (e) => {
        e.preventDefault()
        console.log("Featured prev clicked")
        showFeaturedSlide(featuredCurrentSlide - 1)
      })
    }

    if (featuredNextBtn) {
      featuredNextBtn.addEventListener("click", (e) => {
        e.preventDefault()
        console.log("Featured next clicked")
        showFeaturedSlide(featuredCurrentSlide + 1)
      })
    }

    // Auto slide for featured carousel
    setInterval(() => {
      showFeaturedSlide(featuredCurrentSlide + 1)
    }, 5000)
  }

  // Game Carousels - Fixed to handle multiple carousels properly
  const gameCarousels = document.querySelectorAll(".game-carousel")
  console.log("Found game carousels:", gameCarousels.length)

  gameCarousels.forEach((carousel, index) => {
    const grid = carousel.querySelector(".game-grid")
    const prevBtn = carousel.querySelector(".carousel-arrow.prev")
    const nextBtn = carousel.querySelector(".carousel-arrow.next")

    console.log(`Game carousel ${index}:`, {
      grid: !!grid,
      prevBtn: !!prevBtn,
      nextBtn: !!nextBtn,
    })

    if (grid && prevBtn && nextBtn) {
      const cardWidth = 240 // Card width + gap
      let scrollPosition = 0

      prevBtn.addEventListener("click", (e) => {
        e.preventDefault()
        console.log(`Game carousel ${index} prev clicked`)
        scrollPosition = Math.max(0, scrollPosition - cardWidth * 2)
        grid.scrollTo({
          left: scrollPosition,
          behavior: "smooth",
        })
      })

      nextBtn.addEventListener("click", (e) => {
        e.preventDefault()
        console.log(`Game carousel ${index} next clicked`)
        const maxScroll = grid.scrollWidth - grid.clientWidth
        scrollPosition = Math.min(maxScroll, scrollPosition + cardWidth * 2)
        grid.scrollTo({
          left: scrollPosition,
          behavior: "smooth",
        })
      })

      // Update scroll position when user scrolls manually
      grid.addEventListener("scroll", () => {
        scrollPosition = grid.scrollLeft
      })
    }
  })

  // Buy buttons functionality - Using event delegation
  document.addEventListener("click", (e) => {
    const buyButton = e.target.closest(".buy-button")
    if (buyButton) {
      e.preventDefault()
      const gameCard = buyButton.closest(".game-card")
      const gameName = gameCard.querySelector("h3").textContent
      const gamePrice = gameCard.querySelector(".price").textContent

      console.log("Buy button clicked:", gameName)
      alert(`Added to cart: ${gameName} - ${gamePrice}`)

      // Animation effect
      buyButton.classList.add("clicked")
      setTimeout(() => {
        buyButton.classList.remove("clicked")
      }, 300)
    }
  })

  // Search functionality
  const searchInput = document.querySelector(".search-bar input")
  const searchButton = document.querySelector(".search-bar button")

  function performSearch() {
    const searchTerm = searchInput.value.trim().toLowerCase()
    if (searchTerm === "") return

    console.log("Search performed:", searchTerm)
    alert(`Searching for: ${searchTerm}`)
  }

  if (searchButton) {
    searchButton.addEventListener("click", (e) => {
      e.preventDefault()
      performSearch()
    })
  }

  if (searchInput) {
    searchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        e.preventDefault()
        performSearch()
      }
    })
  }

  // Platform navigation clicks
  const platformLinks = document.querySelectorAll(".platform-nav a")
  platformLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault()
      const platform = link.textContent.trim()
      console.log("Platform clicked:", platform)
      alert(`Filtering by platform: ${platform}`)
    })
  })

  // View all links
  const viewAllLinks = document.querySelectorAll(".view-all")
  viewAllLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault()
      const section = link.closest(".game-section").querySelector("h2").textContent
      console.log("View all clicked:", section)
      alert(`Viewing all games in: ${section}`)
    })
  })

  console.log("All event listeners attached successfully")
})