<template>
  <div class="about">
    <img class="untitled-design-1" alt="" src="/images/Untitled design 1.png">
    <div class="evil-twin-detector-title">EVIL TWIN DETECTOR</div>
    <div class="about-text">
        <p>
            An evil twin attack is an event where a bad actor creates a fake access point that imitates a legitimate one with the aim of collecting user credentials, logins, or other personal data. Evil Twin Detector is designed to help everyday users detect WiFi connections that are suspicious or imitating trusted networks. These networks can be captured using SSL certificates and beacon frames, which would alert users to malicious WiFi before or after connecting. Our mission is to help protect users on all levels by providing tools that make WiFi security accessible to everyone.
        </p>
    </div>
    <div class="creators-section">
        <h2>Creators</h2>
        <ul>
            <li>Patrick Bucknor</li>
            <li>Tajeka Johnson</li>
            <li>Rae-Ann Clarke </li>
            <li>Joelle Mercurius</li>
        </ul>
    </div>
    <img class="spy-img" alt="Spy Art" src="/images/spyvsspy 1.png" />
    <Navbar />
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue'

export default {
  name: 'About',
  components: {
    Navbar
  }
}
</script>

<style scoped>
.about {
  width: 100vw;
  min-height: 100vh;
  background-color: #000dbf;
  position: relative;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  box-sizing: border-box;
  padding-bottom: 80px;
}

.untitled-design-1 {
  display: block;
  margin: 40px auto 0 auto;
  width: 152px;
  height: 177px;
  object-fit: cover;
  position: absolute;
  top: 40px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
}

.evil-twin-detector-title {
  font-family: 'Jost', sans-serif;
  font-size: 48px;
  font-weight: 600;
  color: #fff;
  text-align: center;
  margin-top: 230px;
  margin-bottom: 32px;
  letter-spacing: 0.06em;
  z-index: 2;
}

.about-text {
  max-width: 700px;
  margin: 0 auto 0 auto;
  font-size: 1.25rem;
  color: #fff;
  text-align: left;
  line-height: 1.7;
  z-index: 2;
}

.about-text p {
  margin-bottom: 1.5em;
}

.creators-section {
  margin: 2.5rem auto 1.5rem auto;
  text-align: center;
  z-index: 2;
}

.creators-section h2 {
  font-size: 1.3em;
  margin-bottom: 0.5em;
  color: #fff;
  font-family: 'Jost', sans-serif;
  letter-spacing: 0.04em;
}

.creators-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.creators-section li {
  font-size: 1.1em;
  margin-bottom: 0.3em;
  color: #fff;
}

.spy-img {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 200px;
  object-fit: contain;
  z-index: 1;
}
</style>
