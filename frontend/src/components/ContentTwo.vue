<template>
    <div class="content-card">
        <img
            src="../assets/page2.png"
            alt=""
            width="100%" />
        <i class="fas fa-arrow-down scroll-indicator"></i>
    </div>
</template>
<script></script>
<style scoped>
    .content-card {
        width: 100%;
        height: 100%; /* 让组件在 wrapper 中不会被裁剪、塌陷 */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .scroll-indicator {
        z-index: 100;
        position: fixed;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 40px;
        color: #ffffff;
        animation: bounce 1.5s infinite ease-in-out;
        opacity: 0.9;
    }

    .scroll-indicator:hover {
        opacity: 1;
        color: #000;
    }

    @keyframes bounce {
        0%,
        100% {
            transform: translateX(-50%) translateY(0);
        }
        50% {
            transform: translateX(-50%) translateY(10px);
        }
    }
</style>
