import "./HomePage.css";

function HomePage() {
  return (
    <div className="home-page">
      <header className="navbar">
        <div className="container nav-content">
          <a href="/" className="logo">
            <span className="logo-mark">S</span>
            <span>Shopora</span>
          </a>

          <nav className="nav-links">
            <a href="#home">Home</a>
            <a href="#products">Products</a>
            <a href="#categories">Categories</a>
            <a href="#about">About</a>
          </nav>

          <div className="nav-actions">
            <button className="icon-button">⌕</button>
            <button className="icon-button">🛒</button>
            <button className="login-button">Login</button>
          </div>
        </div>
      </header>

      <main>
        <section className="hero" id="home">
          <div className="container hero-content">
            <div className="hero-text">
              <span className="eyebrow">NEW COLLECTION 2026</span>

              <h1>
                Everything you need.
                <span> All in one place.</span>
              </h1>

              <p>
                Discover carefully selected products designed to make your
                everyday life simpler, smarter, and better.
              </p>

              <div className="hero-actions">
                <a href="#products" className="primary-button">
                  Shop Now →
                </a>

                <a href="#categories" className="secondary-button">
                  Explore Collection
                </a>
              </div>

              <div className="stats">
                <div>
                  <strong>10K+</strong>
                  <span>Products</span>
                </div>

                <div>
                  <strong>25K+</strong>
                  <span>Customers</span>
                </div>

                <div>
                  <strong>4.9/5</strong>
                  <span>Rating</span>
                </div>
              </div>
            </div>

            <div className="hero-visual">
              <div className="hero-product">
                <div className="product-badge">NEW</div>
                <div className="product-object">📱</div>
              </div>

              <div className="floating-card card-top">
                ⭐ 4.9 Rating
              </div>

              <div className="floating-card card-bottom">
                ✓ Free Shipping
              </div>
            </div>
          </div>
        </section>

        <section className="section" id="categories">
          <div className="container">
            <div className="section-header">
              <div>
                <span className="section-label">EXPLORE</span>
                <h2>Shop by category</h2>
              </div>

              <a href="#products">View all →</a>
            </div>

            <div className="category-grid">
              <Category icon="💻" title="Technology" count="240 products" />
              <Category icon="🎧" title="Audio" count="180 products" />
              <Category icon="⌚" title="Wearables" count="120 products" />
              <Category icon="🏠" title="Home" count="320 products" />
            </div>
          </div>
        </section>

        <section className="section products-section" id="products">
          <div className="container">
            <div className="section-header">
              <div>
                <span className="section-label">TRENDING NOW</span>
                <h2>Featured products</h2>
              </div>

              <a href="#products">View all →</a>
            </div>

            <div className="product-grid">
              <Product
                icon="🎧"
                category="Audio"
                name="Wireless Headphones"
                description="Premium sound with active noise cancellation."
                price="$129"
              />

              <Product
                icon="⌚"
                category="Wearables"
                name="Smart Watch Pro"
                description="Stay connected, active, and organized."
                price="$199"
              />

              <Product
                icon="💻"
                category="Technology"
                name="Ultra Laptop"
                description="Powerful performance in a lightweight design."
                price="$899"
              />

              <Product
                icon="📱"
                category="Technology"
                name="Smartphone X"
                description="Next-generation performance and design."
                price="$699"
              />
            </div>
          </div>
        </section>

        <section className="promo">
          <div className="container">
            <div className="promo-card">
              <span className="section-label">LIMITED OFFER</span>

              <h2>Upgrade your everyday.</h2>

              <p>
                Get up to 30% off selected products for a limited time.
              </p>

              <a href="#products" className="promo-button">
                Shop the offer →
              </a>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer" id="about">
        <div className="container footer-content">
          <div>
            <div className="logo footer-logo">
              <span className="logo-mark">S</span>
              <span>Shopora</span>
            </div>

            <p>
              A modern shopping experience built around simplicity,
              quality, and great products.
            </p>
          </div>

          <div className="footer-links">
            <a href="#products">Products</a>
            <a href="#categories">Categories</a>
            <a href="#about">About</a>
            <a href="#about">Contact</a>
          </div>
        </div>

        <div className="container footer-bottom">
          © 2026 Shopora. All rights reserved.
        </div>
      </footer>
    </div>
  );
}

type CategoryProps = {
  icon: string;
  title: string;
  count: string;
};

function Category({ icon, title, count }: CategoryProps) {
  return (
    <div className="category-card">
      <div className="category-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{count}</p>
    </div>
  );
}

type ProductProps = {
  icon: string;
  category: string;
  name: string;
  description: string;
  price: string;
};

function Product({
  icon,
  category,
  name,
  description,
  price,
}: ProductProps) {
  return (
    <article className="product-card">
      <div className="product-image">
        <span>{icon}</span>
        <button className="favorite-button">♡</button>
      </div>

      <div className="product-info">
        <span className="product-category">{category}</span>

        <h3>{name}</h3>

        <p>{description}</p>

        <div className="product-footer">
          <strong>{price}</strong>
          <button className="add-button">+</button>
        </div>
      </div>
    </article>
  );
}

export default HomePage;