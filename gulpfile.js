var concat = require('gulp-concat'),
    gulp = require('gulp'),
    mainBowerFiles = require('main-bower-files'),
    path = require('path');


// Directory where the results go
var output_directory = path.join('fetsy', 'static');


// Catches all JavaScript files from all bower components and concats them to
// one file js/fetsy-libs.js. HTML5 Shiv and Respond.js are excluded.
gulp.task('js', function() {
    return gulp.src(mainBowerFiles({
        filter: function (file) {
                var name = path.basename(file)
                return name !== 'html5shiv.js' && name !== 'respond.src.js' && path.extname(name) == '.js';
            }
        }))
        .pipe(concat('fetsy-libs.js'))
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});


// Catches HTML5 Shiv and Respond.js and moves them to the output directory.
gulp.task('special-js', function () {
    var html5shiv = path.join('bower_components', 'html5shiv', 'dist', 'html5shiv.min.js'),
        respondjs = path.join('bower_components', 'respond', 'dest', 'respond.min.js');
    return gulp.src([html5shiv, respondjs])
        .pipe(gulp.dest(path.join(output_directory, 'js')));
});


// Catches all CSS files from all bower components and concats them to one file
// css/fetsy-libs.css.
gulp.task('css', function() {
    return gulp.src(mainBowerFiles({
        filter: /\.css$/
    }))
    .pipe(concat('fetsy-libs.css'))
    .pipe(gulp.dest(path.join(output_directory, 'css')));
});


// Catches all font files from all bower components.
gulp.task('fonts', function() {
    return gulp.src(mainBowerFiles({
        filter: /\.(eot)|(svg)|(ttf)|(woff)$/
    }))
    .pipe(gulp.dest(path.join(output_directory, 'fonts')));
});

gulp.task('default', ['js', 'special-js', 'css', 'fonts'], function() {});
