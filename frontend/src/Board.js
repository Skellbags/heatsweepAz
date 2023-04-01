export default function Board() {
  const numRows = 10
  const numCols = 10

  // Generate a 2D array filled with zeroes
  let grid = Array.from({ length: numRows }, () => Array.from({ length: numCols }, () => 0))

  // Place a 1 and a 2 in the top-left and bottom-right corners of the grid, respectively
  grid[0][0] = 1
  grid[numRows - 1][numCols - 1] = 2

  // Place a 3 at a random position in the grid
  const row = Math.floor(Math.random() * numRows)
  const col = Math.floor(Math.random() * numCols)
  grid[row][col] = 3

  return {
    grid
  }
}

