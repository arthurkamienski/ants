var canvas, ctx;

var updatedTiles;
var pheromoneTiles;

var board;
var ants;

var maxScentTime = 5000;
var antScentDecay = 0.8;
var tileScentDecay = 0.5;

var foodScentRange = 15;
var nestScentRange = 15;
var fps = 50;

var gridSizeX = 150;
var gridSizeY = 100;

var tileSize = 5;

var nestPos = [15, 15];
var foodPos = [gridSizeX-15, gridSizeY-15];

var startAnts = 30;
var scouts = startAnts;
var maxScouts = startAnts;
var maxAnts = 500;

var showPheromones = true;
var showGrid = false;

var scoutRandomness = 0.5;
var workerRandomness = 0.1;
var scoutSpawnProb = 0.05;

var foodRadius = 2;
var nestRadius = 2;

var backgroundColor = 'white';
var workerColor = 'black';
var nestColor = 'chocolate';
var foodColor = 'darkgreen';
var foodScentColor = '#d1e4c9';
var carrierColor = 'forestGreen';
var scoutColor = 'maroon';

foodPherColors = [
  '#cd9504',
  '#d59f2e',
  '#dca948',
  '#e2b360',
  '#e9be77',
  '#eec88d',
  '#f3d3a3',
  '#f7deba',
  '#fae9d1',
  '#fdf4e8'
]

nestPherColors = [
  '#a304be',
  '#ae35c5',
  '#b951cc',
  '#c369d2',
  '#cd7fd9',
  '#d795e0',
  '#e0aae6',
  '#e8bfec',
  '#f0d4f3',
  '#f8eaf9'
]

$(document).ready(function() {
  start();

  if (showGrid) {
    drawGrid();
  }

  board.tiles.forEach(function(t, k, m) {
    t.init();
    t.draw();
  });

  pheromoneTiles = [];
  
  interval = window.setInterval(function() {
    updatedTiles = pheromoneTiles;
    pheromoneTiles = [];

    for (const a of ants) {
      a.move();
    }

    for (const t of updatedTiles) {
      t.update();
    }
  }, 1000/fps);

});

function start() {
  board = new Board();

  ants = [];

  for (i = 0; i < startAnts; i++) {
    ants.push(new Ant(true));
  }

  canvas = $('#canvas')[0];
  ctx = canvas.getContext("2d");
  canvas.selection = false;
  setCanvasSize();
}

function setCanvasSize() {
  canvas.width  = board.gridSize.x*board.tileSize;
  canvas.height = board.gridSize.y*board.tileSize;

  if (showGrid) {
    canvas.width++;
    canvas.height++;
  }
}

function Board() {
  this.tileSize = tileSize;
  this.gridSize = {x: gridSizeX, y: gridSizeY};
  this.tiles = new Map();

  this.tileAt = function(x, y) {
    return this.tiles.get(y*this.gridSize.x+x);
  }

  for (i=0; i < this.gridSize.x; i++) {
    for (j=0; j < this.gridSize.y; j++) {
      this.tiles.set(j*this.gridSize.x+i, new Tile(i, j));
    }
  }

  this.nest = this.tileAt(nestPos[0], nestPos[1]);
  this.food = this.tileAt(foodPos[0], foodPos[1]);
  this.nest.isNest = true;
  this.food.isFood = true;
}

function Tile(x, y) {
  this.x = x;
  this.y = y;

  this.isNest = false;
  this.isFood = false;
  this.hasAnt = false;
  this.antType = null;
  
  this.nestPher = 0;
  this.foodPher = 0;
  this.scent    = 0;

  this.defaultColor = backgroundColor;
  this.color = this.defaultColor;

  this.init = function() {
    this.neighbors = [
      [this.x+1, this.y],
      [this.x-1, this.y],
      [this.x, this.y+1],
      [this.x, this.y-1]
    ].filter(
      c =>
      c[0] >= 0 &&
      c[1] >= 0 &&
      c[0] < board.gridSize.x &&
      c[1] < board.gridSize.y
    ).map(
      c => board.tileAt(c[0], c[1])
    ).filter(t => typeof t !== "undefined");

    this.scent = Math.max(0, foodScentRange - this.distTo(board.food));

    if (this.distTo(board.food) <= foodRadius) {
      this.isFood = true;
    }

    if (this.distTo(board.nest) <= nestRadius) {
      this.isNest = true;
    }

    if (this.isNest) {
      this.defaultColor = nestColor;
    } else if (this.isFood) {
      this.defaultColor = foodColor;
    } else if (this.scent > 0) {
      this.defaultColor = foodScentColor;
    }

    this.color = this.defaultColor;
  }

  this.update = function() {
    var prevColor = this.color;
    this.foodPher -= tileScentDecay;
    this.nestPher -= tileScentDecay;

    if(!this.isNest && !this.isFood) {
      if (this.hasAnt) {
        if (this.antType == 'worker') {
          this.color = workerColor;
        } else if (this.antType == 'carrier') {
          this.color = carrierColor;
        } else {
          this.color = scoutColor;
        }
      } else if (this.nestPher > 0 && this.nestPher > this.foodPher) {
        if (showPheromones) {
          this.color = nestPherColors[9-Math.floor(this.nestPher/maxScentTime*10)];
        } else {
          this.color = this.defaultColor;
        }

        pheromoneTiles.push(this);
      } else if (this.foodPher > 0) {
        if (showPheromones) {
          this.color = foodPherColors[9-Math.floor(this.foodPher/maxScentTime*10)];
        } else {
          this.color = this.defaultColor;
        }
        
        pheromoneTiles.push(this);
      } else {
        this.color = this.defaultColor;
      }

      if(this.color != prevColor) {
        this.draw();
      }
    }
  }

  this.isEqual = function(other) {
    return this.x == other.x && this.y == other.y;
  }

  this.distTo = function(other) {
    return Math.sqrt(Math.pow(this.x - other.x, 2) +
      Math.pow(this.y - other.y, 2));
  }

  this.draw = function() {
    var size = board.tileSize;

    ctx.fillStyle = this.color;

    if (showGrid) {
      ctx.fillRect(this.x*size+1, this.y*size+1, size-1, size-1);
    } else {
      ctx.fillRect(this.x*size, this.y*size, size, size);
    }

  }
}

function Ant(scouting) {
  this.tile     = board.nest;
  this.lastTile = this.tile;

  this.isScouting = scouting;
  this.hasFood  = false;
  
  this.scentStrength = maxScentTime;

  this.move = function() {
    var nextTile = this.tile;

    var moves = this.tile.neighbors.filter(
      t => !t.isEqual(this.lastTile) && !t.hasAnt
    );

    if (moves.length > 0) {
      nextTile = moves[Math.floor(Math.random() * moves.length)];

      if (this.isScouting) {
        if (Math.random() > scoutRandomness) {
          var withScent = moves.filter(t => t.scent > 0);
          
          if (withScent.length > 0) {
            nextTile = withScent.reduce(function(prev, current) {
              return (prev.scent > current.scent) ? prev : current
            });
          } else {
            nextTile = moves.reduce(function(prev, current) {
              return (prev.nestPher < current.nestPher) ? prev : current
            });
          }
        }
      } else if (this.hasFood) {
        if (Math.random() > workerRandomness) {
          var withScent = moves.filter(t => t.nestPher > 0);

          if (withScent.length > 0) {
            nextTile = withScent.reduce(function(prev, current) {
              return (prev.nestPher > current.nestPher) ? prev : current
            });
          }
        }
      } else {
        if (Math.random() > workerRandomness) {
          var withScent = moves.filter(t => t.foodPher > 0);
  
          if (withScent.length > 0) {
            nextTile = withScent.reduce(function(prev, current) {
              return (prev.foodPher > current.foodPher) ? prev : current
            });
          }
        }
      }

      if (nextTile.isEqual(board.food)) {
        this.scentStrength = maxScentTime;
        this.hasFood = true;
        if (this.isScouting) {
          scouts--;
        }

        this.isScouting = false;
      } else if (nextTile.isEqual(board.nest)) {
        if (this.hasFood) {
          if (ants.length < maxAnts) {
            ants.push(new Ant(false));
          }
          if (Math.random() < scoutSpawnProb && scouts < maxScouts) {
            this.isScouting = true;
            scouts++;
          }
        }

        this.hasFood = false;
        this.scentStrength = maxScentTime;
      }

      this.lastTile = this.tile;
      this.tile = nextTile;
      nextTile.hasAnt = true;
      this.lastTile.hasAnt = false;
      
      updatedTiles.push(this.lastTile);
      updatedTiles.push(nextTile);

      if (this.hasFood) {
        nextTile.antType = 'carrier';
      } else if (this.isScouting) {
        nextTile.antType = 'scout';
      } else {
        nextTile.antType = 'worker';
      }

      this.scentStrength = Math.max(0.1*maxScentTime, this.scentStrength-antScentDecay);

      if (this.hasFood) {
        nextTile.foodPher = Math.max(nextTile.foodPher, this.scentStrength);
      } else {
        nextTile.nestPher = Math.max(nextTile.nestPher, this.scentStrength);
      }
    }
  }
}

function toggleGrid() {
  showGrid = !showGrid;
  setCanvasSize();

  if (showGrid) {
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  board.tiles.forEach(function(t, k, m) {
    t.draw();
  });
}
