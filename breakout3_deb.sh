#!/bin/bash
# Script to build BreakOut3 .deb package for Debian/Ubuntu Linux

set -e  # Exit on error

echo "=========================================="
echo "BreakOut3 Debian Package Builder"
echo "=========================================="
echo ""

# Configuration
APP_NAME="breakout3"
APP_VERSION="1.0.0"
APP_DISPLAY_NAME="BreakOut3"
MAINTAINER="FreqRider <your.email@example.com>"
DESCRIPTION="Classic Breakout arcade game built with Pygame"
ARCH="amd64"  # Change to "arm64" for ARM processors

# Directories
BUILD_DIR="deb_build"
PACKAGE_DIR="${BUILD_DIR}/${APP_NAME}_${APP_VERSION}_${ARCH}"
DEBIAN_DIR="${PACKAGE_DIR}/DEBIAN"
USR_DIR="${PACKAGE_DIR}/usr"
BIN_DIR="${USR_DIR}/local/bin"
SHARE_DIR="${USR_DIR}/share"
APPS_DIR="${SHARE_DIR}/applications"
ICONS_DIR="${SHARE_DIR}/icons/hicolor"
APP_DATA_DIR="${SHARE_DIR}/${APP_NAME}"

echo "Step 1: Cleaning old build files..."
rm -rf ${BUILD_DIR}
rm -f ${APP_NAME}_${APP_VERSION}_${ARCH}.deb

echo "Step 2: Creating directory structure..."
mkdir -p ${DEBIAN_DIR}
mkdir -p ${BIN_DIR}
mkdir -p ${APPS_DIR}
mkdir -p ${ICONS_DIR}/512x512/apps
mkdir -p ${ICONS_DIR}/256x256/apps
mkdir -p ${ICONS_DIR}/128x128/apps
mkdir -p ${ICONS_DIR}/64x64/apps
mkdir -p ${ICONS_DIR}/48x48/apps
mkdir -p ${APP_DATA_DIR}

echo "Step 3: Building PyInstaller binary..."
if [ ! -f "breakout3.spec" ]; then
    echo "Error: breakout3.spec not found!"
    exit 1
fi

# Build with PyInstaller
pyinstaller --clean breakout3.spec

if [ ! -f "dist/BreakOut3/BreakOut3" ]; then
    echo "Error: PyInstaller build failed!"
    exit 1
fi

echo "Step 4: Copying executable and data files..."
# Copy the PyInstaller bundle
cp -r dist/BreakOut3/* ${APP_DATA_DIR}/

# Create wrapper script in /usr/local/bin
cat > ${BIN_DIR}/${APP_NAME} << 'EOF'
#!/bin/bash
# Wrapper script for BreakOut3
cd /usr/share/breakout3
exec ./BreakOut3 "$@"
EOF
chmod +x ${BIN_DIR}/${APP_NAME}

echo "Step 5: Converting and copying icons..."
# Use the existing breakout3.png file
if [ ! -f "breakout3.png" ]; then
    echo "Error: breakout3.png not found in working directory!"
    echo "Please ensure breakout3.png exists before building."
    exit 1
fi

echo "Using breakout3.png to generate icon resolutions..."
# Create multiple resolutions from the source PNG
convert breakout3.png -resize 512x512 ${ICONS_DIR}/512x512/apps/${APP_NAME}.png
convert breakout3.png -resize 256x256 ${ICONS_DIR}/256x256/apps/${APP_NAME}.png
convert breakout3.png -resize 128x128 ${ICONS_DIR}/128x128/apps/${APP_NAME}.png
convert breakout3.png -resize 64x64 ${ICONS_DIR}/64x64/apps/${APP_NAME}.png
convert breakout3.png -resize 48x48 ${ICONS_DIR}/48x48/apps/${APP_NAME}.png
echo "Icons generated successfully!"

echo "Step 6: Creating .desktop file..."
cat > ${APPS_DIR}/${APP_NAME}.desktop << EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=${APP_DISPLAY_NAME}
GenericName=Breakout Game
Comment=${DESCRIPTION}
Exec=${APP_NAME}
Icon=${APP_NAME}
Terminal=false
Categories=Game;ArcadeGame;BlocksGame;
Keywords=breakout;arcade;game;brick;paddle;
StartupNotify=true
EOF

echo "Step 7: Creating DEBIAN control file..."
cat > ${DEBIAN_DIR}/control << EOF
Package: ${APP_NAME}
Version: ${APP_VERSION}
Section: games
Priority: optional
Architecture: ${ARCH}
Maintainer: ${MAINTAINER}
Description: ${DESCRIPTION}
 Classic Breakout arcade game where you control a paddle to
 bounce a ball and destroy bricks. Features colorful graphics,
 sound effects, and multiple difficulty levels.
Depends: libc6, libx11-6, libxext6
EOF

echo "Step 8: Creating post-install script..."
cat > ${DEBIAN_DIR}/postinst << 'EOF'
#!/bin/bash
set -e

# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    update-desktop-database -q /usr/share/applications
fi

# Update icon cache
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor
fi

echo "BreakOut3 installed successfully!"
echo "Run 'breakout3' from terminal or find it in your applications menu."

exit 0
EOF
chmod +x ${DEBIAN_DIR}/postinst

echo "Step 9: Creating pre-remove script..."
cat > ${DEBIAN_DIR}/prerm << 'EOF'
#!/bin/bash
set -e
exit 0
EOF
chmod +x ${DEBIAN_DIR}/prerm

echo "Step 10: Creating post-remove script..."
cat > ${DEBIAN_DIR}/postrm << 'EOF'
#!/bin/bash
set -e

# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    update-desktop-database -q /usr/share/applications
fi

# Update icon cache
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor
fi

exit 0
EOF
chmod +x ${DEBIAN_DIR}/postrm

echo "Step 11: Setting permissions..."
# Set proper permissions
find ${PACKAGE_DIR}/usr -type d -exec chmod 755 {} \;
find ${PACKAGE_DIR}/usr -type f -exec chmod 644 {} \;
chmod +x ${BIN_DIR}/${APP_NAME}
chmod +x ${APP_DATA_DIR}/BreakOut3

echo "Step 12: Building .deb package..."
dpkg-deb --build ${PACKAGE_DIR}

# Move the .deb file to current directory
mv ${BUILD_DIR}/${APP_NAME}_${APP_VERSION}_${ARCH}.deb .

echo ""
echo "=========================================="
echo "SUCCESS!"
echo "=========================================="
echo ""
echo "Package created: ${APP_NAME}_${APP_VERSION}_${ARCH}.deb"
echo ""
echo "To install:"
echo "  sudo dpkg -i ${APP_NAME}_${APP_VERSION}_${ARCH}.deb"
echo ""
echo "To uninstall:"
echo "  sudo apt remove ${APP_NAME}"
echo ""
echo "To test without installing:"
echo "  dpkg-deb -c ${APP_NAME}_${APP_VERSION}_${ARCH}.deb  # List contents"
echo "  lintian ${APP_NAME}_${APP_VERSION}_${ARCH}.deb      # Check for issues"
echo ""