<template>
  <div class="home">
    <div class="vector-parent">
      <img class="frame-child" alt="" src="/images/Vector 2.svg">
      <img class="untitled-design-1" alt="" src="/images/Untitled design 1.png">
      
      <div class="main-content">
        <div class="evil-twin-detector">EVIL TWIN DETECTOR</div>
        <div class="welcome">Welcome</div>
      </div>

      <Navbar />
    </div>
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue'

export default {
  name: 'Home',
  components: {
    Navbar
  }
}
</script>

<style scoped>
.home {
  width: 100%;
  height: 100vh;
  background-color: #fff;
  overflow: hidden;
}

.vector-parent {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  background-color: #000dbf;
  height: 100%;
  padding: 2rem 1rem;
  position: relative;
}

.frame-child {
  position: absolute;
  top: 0;
  left: 0;
  width: 1041px;
  height: 1115px;
  mix-blend-mode: multiply;
  z-index: 0;
}

.untitled-design-1 {
  position: absolute;
  top: 159px;
  right: 50px;
  width: 152px;
  height: 177px;
  object-fit: cover;
  z-index: 1;
}

.main-content {
  text-align: center;
  z-index: 2;
  margin-top: 200px;
  color: white;
}

.evil-twin-detector {
  font-size: 64px;
  font-weight: 500;
  letter-spacing: 0.06em;
  color: #1e0303;
  margin-bottom: 1rem;
}

.welcome {
  font-size: 48px;
  letter-spacing: 0.06em;
  color: #ffffff;
}
</style>
