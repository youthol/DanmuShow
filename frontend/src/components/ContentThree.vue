<template>
    <div class="container">
        <div class="danmu-area" @click="createConfetti($event)">
            <!-- 显示飘动的弹幕 -->
            <div v-for="item in danmus" :key="item.id" class="danmu-text" :style="{
                top: item.top + 'px',
                animationDuration: item.duration + 's',
            }" @animationend="removeDanmu(item.id)" @click.stop="handleDanmuClick($event, item.id)" tabindex="-1">
                {{ item.text }}
            </div>

            <!-- 彩带小片 -->
            <div v-for="(confetti, index) in confettis" :key="confetti.id" class="confetti" :class="confetti.shape"
                :style="getConfettiStyle(confetti)" @animationend="removeConfetti(index)"></div>
        </div>
        <div class="input-area">
            <input v-model="inputText" @keyup.enter="addToPool" placeholder="输入你的毕业计划，我们一起努力！" autocomplete="off"
            spellcheck="false" />
            <button @click="addToPool">添加弹幕</button>
        </div>

    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios';


const inputText = ref('')

const danmus = ref([])
const pool = ref([])

const confettis = ref([])

let danmuId = 0
let confettiId = 0

const colors = [
    '#E63946',
    '#F1FAEE',
    '#A8DADC',
    '#457B9D',
    '#F4A261',
    '#2A9D8F',
    '#FFB703',
]

const MAX_DANMU_COUNT = 10


const usedRows = new Set()

const paddingTop = 40
const paddingBottom = 40
const danmuHeight = 24

const maxRows = Math.floor((window.innerHeight * 0.45 - paddingTop - paddingBottom) / danmuHeight)

function randomTop() {
    if (usedRows.size >= maxRows) {
        // 行数全占用，随机返回安全范围内top
        return (
            paddingTop +
            Math.floor(Math.random() * (window.innerHeight * 0.45 - paddingTop - paddingBottom - danmuHeight))
        )
    }
    let row
    let attempts = 0
    do {
        row = Math.floor(Math.random() * maxRows)
        attempts++
        if (attempts > 100) break
    } while (usedRows.has(row))
    usedRows.add(row)
    return paddingTop + row * danmuHeight
}


let timer = null

function startDanmuLoop() {

    timer = setInterval(() => {
        if (danmus.value.length >= MAX_DANMU_COUNT) return
        if (pool.value.length === 0) return

        const text = pool.value[Math.floor(Math.random() * pool.value.length)]

        danmus.value.push({
            id: danmuId++,
            text,
            top: randomTop(),
            duration: 8 + Math.random() * 4,
        })
    }, 1200)
}

function stopDanmuLoop() {
    if (timer) clearInterval(timer)
}

function removeDanmu(id) {
    const idx = danmus.value.findIndex(d => d.id === id)
    if (idx !== -1) {
        const top = danmus.value[idx].top
        const row = Math.floor(top / danmuHeight)
        usedRows.delete(row)
        danmus.value.splice(idx, 1)
    }
}

function handleDanmuClick(event, id) {
  removeDanmu(id)

  const parentRect = event.currentTarget.parentNode.getBoundingClientRect()
  const clickX = event.clientX - parentRect.left
  const clickY = event.clientY - parentRect.top

  for (let i = 0; i < 20; i++) {
    const size = 6 + Math.random() * 6
    confettis.value.push({
      id: confettiId++,
      x: (Math.random() - 0.5) * 80,
      y: (Math.random() - 0.5) * 80,
      rotate: Math.random() * 360,
      duration: 0.6 + Math.random() * 0.4,
      color: colors[Math.floor(Math.random() * colors.length)],
      size,
      shape: Math.random() > 0.5 ? 'circle' : 'square',
      startX: clickX,
      startY: clickY,
    })
  }

  if (pool.value.length > 0 && danmus.value.length < MAX_DANMU_COUNT) {
    const text = pool.value[Math.floor(Math.random() * pool.value.length)]
    danmus.value.push({
      id: danmuId++,
      text,
      top: randomTop(),
      duration: 8 + Math.random() * 4,
    })
  }
}


function removeConfetti(index) {
    confettis.value.splice(index, 1)
}

function getConfettiStyle(confetti) {
    return {
        '--x': confetti.x + 'px',
        '--y': confetti.y + 'px',
        '--rotate': confetti.rotate + 'deg',
        '--size': confetti.size + 'px',
        '--color': confetti.color,
        '--radius': confetti.shape === 'circle' ? '50%' : '10%',
        animationDuration: confetti.duration + 's',
        left: confetti.startX + 'px',
        top: confetti.startY + 'px',
    }
}

async function addToPool() {
  const text = inputText.value.trim()
  if (!text) return

  try {
    await axios.get('/graduation2025/api/danmus/add', {
      params: { text }
    })
    pool.value.push(text)
    inputText.value = ''
    alert('弹幕发送成功！')
  } catch (err) {
    console.error('发送弹幕失败', err)
    alert('发送失败，请重试')
  }
}

async function fetchDanmuPool() {
    try {
        const res = await axios.get('/graduation2025/api/danmus')
        pool.value = res.data.list.map(d => d.text)
    } catch (e) {
        console.error('获取弹幕失败', e)
    }
    pool.value.push("🎉🎉点击弹幕获取好运！")
}

onMounted(() => {
    fetchDanmuPool().then(() => {
        startDanmuLoop()
    })
})

onBeforeUnmount(() => {
    stopDanmuLoop()
})
</script>

<style scoped>
.container {
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    user-select: none;
}

.danmu-area {
    padding: 40px 0;
    position: relative;
    height: 50vh;
    overflow: hidden;
    cursor: default;
}

.danmu-text {
    position: absolute;
    white-space: nowrap;
    color: white;
    font-weight: bold;
    font-size: 22px;
    user-select: none;
    pointer-events: auto;
    animation-name: danmu-move;
    animation-timing-function: linear;
    animation-fill-mode: forwards;
    cursor: pointer;
    outline: none;
    left: 100%;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
}

@keyframes danmu-move {
    from {
        transform: translateX(0);
    }

    to {
        transform: translateX(calc(-100vw - 200px));
    }
}

.confetti {
    position: absolute;
    background-color: var(--color);
    width: var(--size);
    height: var(--size);
    border-radius: var(--radius);
    animation-name: confetti-fly;
    animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    animation-duration: var(--duration, 0.2);
    animation-fill-mode: forwards;
    opacity: 1;
    transform-origin: center;
    pointer-events: none;
}

@keyframes confetti-fly {
    0% {
        opacity: 1;
        transform: translate(0, 0) rotate(0deg) scale(0.3);
    }

    30% {
        opacity: 1;
        transform: translate(calc(var(--x) / 3), calc(var(--y) / 3)) rotate(calc(var(--rotate) / 3)) scale(1);
    }

    100% {
        opacity: 1;
        transform: translate(var(--x), var(--y)) rotate(var(--rotate)) scale(1);
    }
}

.input-area {
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.input-area input {
    flex: 1;
    height: 40px;
    padding: 0 12px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    outline: none;
}

.input-area button {
    width: 80px;
    height: 40px;
    border: none;
    background-color: #457b9d;
    color: #fff;
    border-radius: 4px;
    cursor: pointer;
    user-select: none;
}

.input-area button:hover {
    background-color: #1d3557;
}
</style>
