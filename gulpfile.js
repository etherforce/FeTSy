/**
 * Initial variables.
 */

var coffee = require('gulp-coffee'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    gulpFilter = require('gulp-filter'),
    jshint = require('gulp-jshint'),
    mainBowerFiles = require('main-bower-files'),
    minifyCSS = require('gulp-minify-css'),
    path = require('path'),
    uglify = require('gulp-uglify');


/**
 * Helper objects.
 */

// Directory where the results go
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
 * HTML files.
 */

// Catches fetsy.html and copies it to the output directory.
gulp.task('html', function () {
    return gulp.src(path.join('fetsy','fetsy.html'))
        .pipe(gulp.dest(path.join(output_directory)));
});


/**
 * JavaScript files.
 */

gulp.task('js-all', ['js', 'js-special', 'js-libs', 'js-libs-special'], function () {});

// Catches all JavaScript files for this project and concats them to one
// file js/fetsy.js. The file ie10-viewport-bug-workaround.js is excluded.
gulp.task('js', function () {
    return gulp.src(path.join('fetsy', 'scripts', '*.js'))
        .pipe(gulpFilter(['*', '!ie10-viewport-bug-workaround.js']))
        .pipe(concat('fetsy.js'))
        .pipe(uglify())
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});

// Catches ie10-viewport-bug-workaround.js and copies it to the output
// directory.
gulp.task('js-special', function () {
    return gulp.src(path.join('fetsy', 'scripts', 'ie10-viewport-bug-workaround.js'))
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});

// Catches all JavaScript files from all bower components and concats them
// to one file js/fetsy-libs.js. HTML5 Shiv and Respond.js are excluded.
gulp.task('js-libs', function () {
    return gulp.src(mainBowerFiles({ filter: specialJSFilter(true) }))
        .pipe(concat('fetsy-libs.js'))
        .pipe(uglify())
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});

// Catches HTML5 Shiv and Respond.js and copies them to the output directory.
gulp.task('js-libs-special', function () {
    return gulp.src(mainBowerFiles({ filter: specialJSFilter(false) }))
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});


/**
 * CSS and font files.
 */

gulp.task('css-all', ['css', 'css-libs', 'fonts-libs'], function () {});

// Catches all CSS files for this project and concats them to one
// file css/fetsy.css. The file ie10-viewport-bug-workaround.js is excluded.
gulp.task('css', function () {
    return gulp.src(path.join('fetsy', 'styles', '*.css'))
        .pipe(concat('fetsy.css'))
        .pipe(minifyCSS())
        .pipe(gulp.dest(path.join(output_directory, 'css')));
});

// Catches all CSS files from all bower components and concats them to one
// file css/fetsy-libs.css.
gulp.task('css-libs', function () {
    return gulp.src(mainBowerFiles({
            filter: /\.css$/
        }))
        .pipe(concat('fetsy-libs.css'))
        .pipe(minifyCSS())
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
 * Gulp default task.
 */

gulp.task('default', ['html', 'js-all', 'css-all'], function() {});


/**
 * Helper tasks.
 */

// Checks JavaScript using JSHint.
gulp.task('jshint', function () {
    return gulp.src(['gulpfile.js', path.join('fetsy', 'scripts', '*.js')])
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

// Compiles Literate CoffeeScript to JavaScript.

gulp.task('coffee', function () {
    return gulp.src(path.join('fetsy', 'scripts', '*.md'))
        .pipe(coffee({
            literate: true
        }))
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});

// Watches changes on project's HTML, JavaScript and CSS.
gulp.task('watch', function () {
  gulp.watch(path.join('fetsy', 'fetsy.html'), ['html']);
  gulp.watch(path.join('fetsy', 'scripts', '*.js'), ['js']);
  gulp.watch(path.join('fetsy', 'styles', '*.css'), ['css']);
});
