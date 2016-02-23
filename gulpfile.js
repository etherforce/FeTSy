/**
 * Initial variables.
 */

// TODO: Remove the next line when support for Node 0.10.x is dropped.
// See https://github.com/postcss/postcss#nodejs-010-and-the-promise-api
require('es6-promise').polyfill();

var argv = require('yargs').argv,
    coffee = require('gulp-coffee'),
    coffeelint = require('gulp-coffeelint'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    gulpif = require('gulp-if'),
    jshint = require('gulp-jshint'),
    mainBowerFiles = require('main-bower-files'),
    cssnano = require('gulp-cssnano'),
    rename = require('gulp-rename'),
    path = require('path'),
    uglify = require('gulp-uglify');


/**
 * Helper objects.
 */

// Function to check production mode.
var runsInProductionMode = function () {
    return argv.production;
};

// Directory where the results go.
var output_directory = path.join('dist');

// Filter for some special JavaScript libraries: HTML5 Shiv and Respond.js.
var specialJSFilter = function (exclude) {
    return function (file) {
        var name = path.basename(file);
        if (exclude) {
            return name !== 'html5shiv.js' && name !== 'respond.src.js' && path.extname(name) == '.js';
        } else {
            return name === 'html5shiv.js' || name == 'respond.src.js';
        }
    };
};


/**
 * Webclient HTML files.
 */

// Catches fetsy.html and copies it to the output directory.
gulp.task('html', function () {
    return gulp.src(path.join('fetsy', 'webclient', 'fetsy.html'))
        .pipe(rename('index.html'))
        .pipe(gulp.dest(path.join(output_directory)));
});


/**
 * Webclient JavaScript files.
 */

gulp.task('js-all', ['coffee', 'js-special', 'js-libs', 'js-libs-special'], function () {});

// Catches all CoffeeScript files for this project, compiles Literate
// CoffeeScript to JavaScript and concats the file to one file js/fetsy.js.
gulp.task('coffee', function () {
    return gulp.src(path.join('fetsy', 'webclient', 'scripts', '*.coffee.md'))
        .pipe(coffee({ literate: true }))
        .pipe(concat('fetsy.js'))
        .pipe(gulpif(runsInProductionMode(), uglify()))
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});

// Catches ie10-viewport-bug-workaround.js and copies it to the output
// directory.
gulp.task('js-special', function () {
    return gulp.src(path.join('fetsy', 'webclient', 'scripts', 'ie10-viewport-bug-workaround.js'))
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});

// Catches all JavaScript files from all bower components and concats them
// to one file js/fetsy-libs.js. HTML5 Shiv and Respond.js are excluded.
gulp.task('js-libs', function () {
    return gulp.src(mainBowerFiles({ filter: specialJSFilter(true) }))
        .pipe(concat('fetsy-libs.js'))
        .pipe(gulpif(runsInProductionMode(), uglify()))
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});

// Catches HTML5 Shiv and Respond.js and copies them to the output directory.
gulp.task('js-libs-special', function () {
    return gulp.src(mainBowerFiles({ filter: specialJSFilter(false) }))
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});


/**
 * Webclient CSS and font files.
 */

gulp.task('css-all', ['css', 'css-libs', 'fonts-libs'], function () {});

// Catches all CSS files for this project and concats them to one
// file css/fetsy.css.
gulp.task('css', function () {
    return gulp.src(path.join('fetsy', 'webclient', 'styles', '*.css'))
        .pipe(concat('fetsy.css'))
        .pipe(gulpif(runsInProductionMode(), cssnano()))
        .pipe(gulp.dest(path.join(output_directory, 'css')));
});

// Catches all CSS files from all bower components and concats them to one
// file css/fetsy-libs.css.
gulp.task('css-libs', function () {
    return gulp.src(mainBowerFiles({ filter: /\.css$/ }))
        .pipe(concat('fetsy-libs.css'))
        .pipe(gulpif(runsInProductionMode(), cssnano()))
        .pipe(gulp.dest(path.join(output_directory, 'css')));
});

// Catches all font files from all bower components.
gulp.task('fonts-libs', function () {
    return gulp.src(mainBowerFiles({
            filter: /\.(eot)|(svg)|(ttf)|(woff)|(woff2)$/
        }))
        .pipe(gulp.dest(path.join(output_directory, 'fonts')));
});


/**
 * Crossbar.io configuration
 */

// Catches Crossbar.io configuration file config.json and copies it to the crossbar directory (CBDIR)
gulp.task('crossbar', function () {
    return gulp.src(path.join('fetsy', 'crossbar', 'config.json'))
        .pipe(gulp.dest(path.join('.crossbar')));
});


/**
 * Gulp default task.
 */

gulp.task('default', ['html', 'js-all', 'css-all', 'crossbar'], function () {});


/**
 * Helper tasks.
 */

// Checks JavaScript using JSHint.
gulp.task('jshint', function () {
    return gulp.src(['gulpfile.js', path.join('fetsy', 'webclient', 'scripts', '*.js')])
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

// Checks CoffeeScript using CoffeeLint.
gulp.task('coffeelint', function () {
    return gulp.src(path.join('fetsy', 'webclient', 'scripts', '*.coffee.md'))
        .pipe(coffeelint({ indentation: { value: 4 } }))
        .pipe(coffeelint.reporter('default'));
});

// Checks JavaScript and CoffeeScript.
gulp.task('hint', ['jshint', 'coffeelint'], function () {});

// Watches changes on project's HTML, JavaScript and CSS.
gulp.task('watch', function () {
    gulp.watch(path.join('fetsy', 'webclient', 'fetsy.html'), ['html']);
    gulp.watch(path.join('fetsy', 'webclient', 'scripts', '*.coffee.md'), ['coffee']);
    gulp.watch(path.join('fetsy', 'webclient', 'styles', '*.css'), ['css']);
    gulp.watch(path.join('fetsy', 'crossbar', 'config.json'), ['crossbar']);
});
