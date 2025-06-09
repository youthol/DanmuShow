<template>
  <div class="fixed-background-container"
       @touchstart="handleTouchStart"
       @touchmove="handleTouchMove"
       @touchend="handleTouchEnd">

    <!-- 固定不变的背景部分 -->
    <div class="background-image"></div>

    <!-- 随着滑动更换的内部内容部分 -->
    <div class="content-wrapper">
      <!-- 这里使用 <component> 动态渲染内容 -->
      <transition :name="transitionName" mode="out-in">
        <component :is="currentContentComponent" :key="currentIndex"></component>
      <!-- <ContentOne></ContentOne> -->
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// 导入你的内容组件
import ContentOne from './components/ContentOne.vue';
import ContentTwo from './components/ContentTwo.vue';
import ContentThree from './components/ContentThree.vue';

// --- Reactive State ---
const currentIndex = ref(0);
const contentComponents = [ContentOne, ContentTwo, ContentThree];
const startX = ref(0);
const startY = ref(0);
const endX = ref(0);
const endY = ref(0);
const threshold = 50; // 滑动距离阈值，超过这个值才算有效滑动
const transitionName = ref('slide-left'); // 初始过渡方向

// --- Computed Properties ---
let currentContentComponent = computed(() => {
  return contentComponents[currentIndex.value];
});

// --- Methods (Functions) ---
const handleTouchStart = (event) => {
  startX.value = event.touches[0].clientX;
  startY.value = event.touches[0].clientY;
};

const handleTouchMove = (event) => {
  // 阻止默认的滚动行为，以实现横向滑动翻页
  // 如果你希望页面同时支持纵向滚动，需要更复杂的逻辑来判断滑动方向
  // event.preventDefault();
  endX.value = event.touches[0].clientX;
  endY.value = event.touches[0].clientY;
};

const handleTouchEnd = () => {
  const diffX = endX.value - startX.value;
  const diffY = endY.value - startY.value;

  if (Math.abs(diffY) > Math.abs(diffX) && Math.abs(diffY) > threshold) {
    if (diffY > 0) {
      // 向下滑动 (上一页)
      goToPrevPage();
    } else {
      // 向上滑动 (下一页)
      goToNextPage();
    }
  }

  startX.value = 0;
  startY.value = 0;
  endX.value = 0;
  endY.value = 0;
};

const goToNextPage = () => {  
  if (currentIndex.value < contentComponents.length - 1) {
    transitionName.value = 'slide-up'; // 设置向上滑动过渡
    currentIndex.value++;
  }
};

const goToPrevPage = () => {
  if (currentIndex.value > 0) {
    transitionName.value = 'slide-down'; // 设置向下滑动过渡
    currentIndex.value--;
  }
};

</script>

<style scoped>
.fixed-background-container {
  position: relative;
  overflow: hidden; /* 防止内容溢出，特别是滑动时 */
  touch-action: pan-y; /* 允许纵向滚动，但阻止默认的横向滚动，以便我们处理 */
  /* 或者 touch-action: none; 来完全禁用所有默认触摸行为，如果你完全由JS控制 */
}

.background-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('./assets/bg.jpg'); /* 替换为你的背景图片路径 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
}

.content-wrapper {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  border-radius: 8px;
  text-align: center;
  height: calc(95vh); /* 留出一些边距 */
  display: flex;
  flex-direction: column;
  justify-content: center; /* 让内容居中 */
  align-items: center; /* 确保内容在容器中居中 */
  overflow: hidden; /* 确保组件过渡时不会溢出 */
}

/* 过渡效果 */
.slide-up-enter-active, .slide-up-leave-active,
.slide-down-enter-active, .slide-down-leave-active {
  transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.slide-up-enter-from {
  transform: translateY(100%);
}
.slide-up-leave-to {
  transform: translateY(-100%);
}

.slide-down-enter-from {
  transform: translateY(-100%);
}
.slide-down-leave-to {
  transform: translateY(100%);
}

</style>
