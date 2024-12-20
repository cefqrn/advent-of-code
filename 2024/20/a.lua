--[[
  https://www.lua.org/pil/contents.html
  https://www.lua.org/manual/5.4/
  https://create.roblox.com/docs/luau/metatables
  https://luau.org/typecheck
  https://stackoverflow.com/questions/154672/what-can-i-do-to-increase-the-performance-of-a-lua-program
  https://www.lua.org/gems/sample.pdf

  run with
    20/a.lua
--]]

local abs = math.abs
local insert = table.insert
local remove = table.remove

local Vec2 = {}
Vec2.__index = Vec2

function Vec2.new(x, y)
  return setmetatable({x = x, y = y}, Vec2)
end

function Vec2:adjacent()
  return {
    Vec2.new(self.x,   self.y-1),
    Vec2.new(self.x+1, self.y  ),
    Vec2.new(self.x,   self.y+1),
    Vec2.new(self.x-1, self.y  )
  }
end

function Vec2:distance_to(other)
  return abs(self.x - other.x) + abs(self.y - other.y)
end

function Vec2:nearby(distance)
  local result = {}
  for dx=-distance, distance do
    for dy=-distance, distance do
      local npos = self + Vec2.new(dx, dy)
      local d = self:distance_to(npos)
      if 0 < d and d <= distance then
        insert(result, npos)
      end
    end
  end

  return result
end

function Vec2:__add(other)
  return Vec2.new(self.x + other.x, self.y + other.y)
end

function Vec2:__tostring()
  return string.format("(%d, %d)", self.x, self.y)
end

function Vec2:hash()
  return self.x*999 + self.y
  -- return tostring(self)
end

-- min heap
local Heap = {}
Heap.__index = Heap

function Heap.new(cmp)
  return setmetatable({
    _cmp = cmp or function(a, b) return a - b end
  }, Heap)
end

function Heap:cmp(i, j)
  return self._cmp(self[i], self[j])
end

function Heap:swap(i, j)
  self[i], self[j] = self[j], self[i]
end

function Heap:upheap(i)
  local parent = math.floor(i/2)
  if parent == 0 then return end

  if self:cmp(i, parent) < 0 then
    self:swap(i, parent)
    self:upheap(parent)
  end
end

function Heap:downheap(i)
  local l, r = 2*i, 2*i+1
  if l > #self then return end

  local child = l
  if r <= #self and self:cmp(l, r) > 0 then
    child = r
  end

  if self:cmp(i, child) > 0 then
    self:swap(i, child)
    self:downheap(child)
  end
end

function Heap:insert(o)
  insert(self, o)
  self:upheap(#self)
end

function Heap:remove(o)
  local result = self[1]
  self[1] = remove(self)
  self:downheap(1)
  return result
end

function Heap:format(i, depth)
  local s = string.rep("  ", depth) .. tostring(self[i]) .. "\n"

  if #self >= 2*i   then s = s .. self:format(2*i,   depth+1) end
  if #self >= 2*i+1 then s = s .. self:format(2*i+1, depth+1) end

  return s
end

function Heap:__tostring()
  return self:format(1, 0)
end

local function is_valid_position(grid, pos)
  local v = grid[pos:hash()]
  return v and v ~= "#"
end

local function distances_from(grid, pos)
  local distances = {[pos:hash()] = 0}

  local remaining = Heap.new(function(a, b) return a[1] - b[1] end)
  remaining:insert({0, pos})
  repeat
    local cost, pos = table.unpack(remove(remaining))
    for _, npos in ipairs(pos:adjacent()) do
      if is_valid_position(grid, npos) and not distances[npos:hash()] then
        distances[npos:hash()] = cost + 1
        remaining:insert({cost+1, npos})
      end
    end
  until #remaining == 0

  return distances
end

local function solve(grid, ipos, epos, cheat_time)
  local distances_from_start = distances_from(grid, ipos)
  local distances_from_end   = distances_from(grid, epos)

  local without_cheating = distances_from_end[ipos:hash()]

  local result = 0
  for x=1, grid.w do
    for y=1, grid.h do
      local pos = Vec2.new(x, y)
      if is_valid_position(grid, pos) then
        for _, npos in ipairs(pos:nearby(cheat_time)) do
          if is_valid_position(grid, npos) then
            local cost = distances_from_start[pos:hash()] + pos:distance_to(npos) + distances_from_end[npos:hash()]
            if cost <= without_cheating - 100 then
              result = result + 1
            end
          end
        end
      end
    end
  end

  return result
end

local ipos, epos

local grid = {}
local y = 0
for line in io.lines("input") do
  local x = 0
  while true do
    local c = string.sub(line, x+1, x+1)

    if c == "" then break end
    x = x + 1

    grid.w = grid.w and math.max(grid.w, x) or x

    local pos = Vec2.new(x, y+1)
    if c == "S" then ipos = pos end
    if c == "E" then epos = pos end

    grid[pos:hash()] = c
  end

  if x == 0 then break end
  y = y + 1
end

grid.h = y

print(solve(grid, ipos, epos, 2))
print(solve(grid, ipos, epos, 20))
