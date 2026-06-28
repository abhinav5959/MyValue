/**
 * MyValue Platform — Frontend Interaction Control Engine
 * Handles scroll-snapping section visibility, active state toggles,
 * liquid glass contrast filtering, and the floating arrow control bubble.
 */

document.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector(".master-scroll-container");
    const sections = document.querySelectorAll(".viewport-snap-block");
    const navLinks = document.querySelectorAll(".nav-link-item");
    const body = document.body;
    const scrollTopArrowBtn = document.getElementById("scrollTopArrowBtn");

    // ==========================================================================
    // 1. Intersection Observer for Chromodynamic & Liquid Glass Windows
    // ==========================================================================
    
    // Configure structural parameters: trigger whenever a section takes up 50%+ of the screen
    const observerOptions = {
        root: container,
        rootMargin: "0px",
        threshold: 0.5
    };

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const activeSectionIndex = entry.target.getAttribute("data-section");
                
                // Remove existing active viewport flags from all layout modules
                sections.forEach(sec => sec.classList.remove("active-in-view"));
                
                // Activate high-contrast liquid glass filter on the current block
                entry.target.classList.add("active-in-view");

                // Update the master body flag to trigger the background core dimming curves
                body.className = `active-section-${activeSectionIndex}`;

                // Coordinate active tab indicator line states in the nav pod
                navLinks.forEach(link => {
                    if (link.getAttribute("data-target") === activeSectionIndex) {
                        link.classList.add("active");
                    } else {
                        link.classList.remove("active");
                    }
                });

                // Handle conditional visibility of the scroll-to-top floating control tile
                if (activeSectionIndex !== "1") {
                    scrollTopArrowBtn.classList.add("visible");
                } else {
                    scrollTopArrowBtn.classList.remove("visible");
                }
            }
        });
    }, observerOptions);

    // Bind scroll monitoring nodes
    sections.forEach(section => sectionObserver.observe(section));

    // ==========================================================================
    // 2. Asynchronous Form Handler Setup Placeholder (Future Supabase Link)
    // ==========================================================================
    const contactForm = document.getElementById("contactTerminalForm");
    
    if (contactForm) {
        contactForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            
            // Gather input fields from the terminal form layout
            const name = document.getElementById("userName").value;
            const email = document.getElementById("userEmail").value;
            const message = document.getElementById("userMessage").value;
            
            const submitButton = contactForm.querySelector(".solar-corona-btn");
            const originalButtonText = submitButton.innerHTML;
            
            // Provide localized tactile loading feedback on click execution
            submitButton.disabled = true;
            submitButton.innerHTML = "Routing Payload...";
            
            /**
             * NOTE: Your Supabase client instantiation and direct REST fetch link 
             * will be wired directly right here during the cloud hosting phase.
             * * Example Blueprint:
             * const response = await fetch('YOUR_SUPABASE_URL/rest/v1/messages', {
             * method: 'POST',
             * headers: {
             * 'apikey': 'YOUR_SUPABASE_ANON_KEY',
             * 'Authorization': 'Bearer YOUR_SUPABASE_ANON_KEY',
             * 'Content-Type': 'application/json'
             * },
             * body: JSON.stringify({ name, email, message })
             * });
             */
            
            setTimeout(() => {
                // Return successful validation status to user experience layer without page wipe
                alert(`System Notification:\nMessage logged from ${name}. Connection string validated!`);
                
                // Clear fields and restore button state
                contactForm.reset();
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
            }, 800);
        });
    }
});