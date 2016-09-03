argv = require 'yargs'
    .argv
cleanCSS = require 'gulp-cleancss'
coffee = require 'gulp-coffee'
coffeelint = require 'gulp-coffeelint'
concat = require 'gulp-concat'
gulp = require 'gulp'
gulpif = require 'gulp-if'
jshint = require 'gulp-jshint'
lazypipe = require 'lazypipe'
mainBowerFiles = require 'main-bower-files'
path = require 'path'
rename = require 'gulp-rename'
sass = require 'gulp-sass'
sourcemaps = require 'gulp-sourcemaps'
templateCache = require 'gulp-angular-templatecache'
uglify = require 'gulp-uglify'


# Helpers and config

productionMode = argv.production

outputDirectory = path.join __dirname, 'dist'


# Gulp default task

gulp.task 'default', ['index', 'js', 'css', 'crossbar'], ->


# Main index file

gulp.task 'index', ->
    gulp.src path.join 'fetsy', 'webclient', 'fetsy.html'
        .pipe rename 'index.html'
        .pipe gulp.dest path.join outputDirectory


# JavaScript files

gulp.task 'js', [
    'coffee'
    'templates'
    'js-extra'
    'js-libs'
], ->

gulp.task 'coffee', ->
    gulp.src path.join 'fetsy', 'webclient', 'scripts', '**', '*.coffee.md'
    .pipe sourcemaps.init()
    .pipe coffee
        literate: true
    .pipe concat 'fetsy.js'
    .pipe sourcemaps.write()
    .pipe gulpif productionMode, uglify()
    .pipe gulp.dest path.join outputDirectory, 'js'

gulp.task 'templates', ->
    gulp.src path.join 'fetsy', 'webclient', 'templates', '**', '*.html'
    .pipe templateCache 'fetsy-templates.js',
        module: 'FeTSy-templates'
        standalone: true
        moduleSystem: 'IIFE'
    .pipe gulpif productionMode, uglify()
    .pipe gulp.dest path.join outputDirectory, 'js'

gulp.task 'js-extra', ->
    gulp.src path.join 'fetsy', 'webclient', 'static', 'js', '*.js'
    .pipe sourcemaps.init()
    .pipe concat 'fetsy-extra.js'
    .pipe sourcemaps.write()
    .pipe gulpif productionMode, uglify()
    .pipe gulp.dest path.join outputDirectory, 'js'

gulp.task 'js-libs', ->
    isntSpecialFile = (file) ->
        name = path.basename file.path
        name isnt 'html5shiv.min.js' and name isnt 'respond.min.js'
    concatChannel = lazypipe()
        .pipe sourcemaps.init
        .pipe concat, 'fetsy-libs.js'
        .pipe sourcemaps.write
    gulp.src mainBowerFiles
        filter: /\.js$/
    .pipe gulpif isntSpecialFile, concatChannel()
    .pipe gulpif productionMode, uglify()
    .pipe gulp.dest path.join outputDirectory, 'js'


# CSS and font files

gulp.task 'css', [
    'sass'
    # 'css-extra'
    'css-libs'
    'fonts-libs'
], ->

gulp.task 'sass', ->
    gulp.src path.join 'fetsy', 'webclient', 'styles', '**', '*.scss'
    .pipe sourcemaps.init()
    .pipe sass().on 'error', sass.logError
    .pipe concat 'fetsy.css'
    .pipe sourcemaps.write()
    .pipe gulp.dest path.join outputDirectory, 'css'

gulp.task 'css-extra', ->
    gulp.src path.join 'fetsy', 'webclient', 'static', 'css', '*.css'
    .pipe sourcemaps.init()
    .pipe concat 'fetsy-extra.css'
    .pipe sourcemaps.write()
    .pipe gulpif productionMode, cleanCSS
        compatibility: 'ie8'
    .pipe gulp.dest path.join outputDirectory, 'css'

gulp.task 'css-libs', ->
    gulp.src mainBowerFiles
        filter: /\.css$/
    .pipe sourcemaps.init()
    .pipe concat 'fetsy-libs.css'
    .pipe sourcemaps.write()
    .pipe gulpif productionMode, cleanCSS
        compatibility: 'ie8'
    .pipe gulp.dest path.join outputDirectory, 'css'

gulp.task 'fonts-libs', ->
    gulp.src mainBowerFiles
        filter: /\.(eot)|(svg)|(ttf)|(woff)|(woff2)$/
    .pipe gulp.dest path.join outputDirectory, 'fonts'


# Crossbar.io configuration

gulp.task 'crossbar', ->
    gulp.src path.join 'fetsy', 'crossbar', 'config.yaml'
    .pipe gulp.dest path.join '.crossbar'


# Helper tasks.

gulp.task 'watch', ['index', 'coffee', 'templates', 'sass', 'crossbar'], ->
    gulp.watch path.join('fetsy', 'webclient', 'fetsy.html'),
        ['index']
    gulp.watch path.join('fetsy', 'webclient', 'scripts', '**', '*.coffee.md'),
        ['coffee']
    gulp.watch path.join('fetsy', 'webclient', 'templates', '**', '*.html'),
        ['templates']
    gulp.watch path.join('fetsy', 'webclient', 'styles', '**', '*.scss'),
        ['sass']
    gulp.watch path.join('fetsy', 'crossbar', 'config.yaml'),
        ['crossbar']
    return

gulp.task 'hint', ['jshint', 'coffeelint'], ->

gulp.task 'jshint', ->
    gulp.src path.join 'fetsy', 'webclient', 'static', 'js', '*.js'
        .pipe jshint()
        .pipe jshint.reporter 'default'

gulp.task 'coffeelint', ->
    gulp.src ['gulpfile.coffee', path.join 'fetsy', 'webclient', 'scripts', '*.coffee.md']
        .pipe coffeelint
            indentation:
                value: 4
        .pipe coffeelint.reporter 'default'
